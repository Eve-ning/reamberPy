from __future__ import annotations

import pandas as pd

from reamber.algorithms.utils import dominant_bpm
from reamber.base import Map


def scroll_speed(m: Map, override_bpm: float = None) -> pd.Series:
    """ Finds the Scroll Speed of the map, with respect to the most active bpm

    Args:
        m: Any Map Instance
        override_bpm: The BPM to replace the most active bpm value.

    Returns:
        A pd.Series of the offset index with values of the scroll speed.
    """
    has_sv = hasattr(m, 'svs')
    offset_min, offset_max = m.stack().offset.min(), m.stack().offset.max()

    df = (
        # Get BPMs
        pd.concat(
            [m.bpms.loc[:, ['offset', 'bpm']],
             # Append Head and Tail offset
             pd.DataFrame(
                 {'offset': [offset_min, offset_max],
                  'bpm': [None, None]}
             )], ignore_index=True
        )
        # Sort by Offset (due to head and tail out of order)
        .sort_values('offset')
        # Assume Head Tail same bpm as nearest
        .ffill().bfill().drop_duplicates()
    )

    if has_sv:
        df_sv = (
            # Get SVs
            pd.concat(
                [
                    # BPMs implicitly reset SV to 1.
                    pd.DataFrame(
                        {'offset': m.bpms.offset,
                         'multiplier': 1}
                    ),
                    pd.DataFrame(
                        {'offset': [offset_min, offset_max],
                         'multiplier': [1, None]}
                    ),
                    m.svs.loc[:, ['offset', 'multiplier']],
                ], ignore_index=True
            )
            # Some offsets can have multiple SVs (because of our implicit BPM 1.0 SV)
            # We'll take the last sv (which has the highest precedence)
            .groupby('offset')
            .last()
            # The end SV is not evaluated until now, so we forward fill
            .ffill()
            # Retrieve offset as column
            .reset_index()
        )

        df = (
            pd.merge(df, df_sv,
                     # Outer Join on SV and BPM
                     on='offset', how='outer')
            # Make sure to sort offset before filling
            .sort_values('offset')
            # Fill in gaps made by OUTER JOIN
            .ffill().bfill()
        )

    # Calculate intervals
    df_interval = df.assign(interval=lambda x: x.offset.diff().shift(-1))

    bpm = override_bpm if override_bpm else dominant_bpm(m)

    # Evaluate Speed
    return df_interval.assign(
        # We take the bpm x sv for the final speed if svs exist
        speed=lambda x: x.bpm / bpm * (x.multiplier if has_sv else 1),
    ).set_index('offset')['speed']

# # # We'll evaluate the visual complexity given by the function above.
# # vc=lambda x: visual_complexity(x.speed),
# # # Weight the Visual Complexity Index by the Proportional Interval
# # # We weight by the proportion, so the output range is [0, 1]
# # w_vc=lambda x: x.vc * x.interval / x.interval.sum()
# def visual_complexity(s):
#     # Formula
#     # \left\{x\ge0:\frac{3}{4}\left(xe^{1-x}+0.5\right)^{-1}-\frac{1}{2}\right\}
#     return 3 / 4 * (s * np.exp(1 - s) + 0.5) ** -1 - 1 / 2

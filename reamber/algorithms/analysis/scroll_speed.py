from __future__ import annotations

import numpy as np
import pandas as pd

from reamber.osu.OsuMap import OsuMap
from reamber.quaver import QuaMap


def scroll_speed(m: OsuMap | QuaMap) -> pd.Series:
    offset_min, offset_max = m.stack().offset.min(), m.stack().offset.max()

    df_ = (
        pd.merge(
            # Get BPMs
            pd.concat(
                [m.bpms[['offset', 'bpm']].df,
                 # Append Head and Tail offset
                 pd.DataFrame(
                     {'offset': [offset_min, offset_max],
                      'bpm': [None, None]}
                 )], ignore_index=True
            )
            # Sort by Offset (due to head and tail out of order)
            .sort_values('offset')
            # Assume Head Tail same bpm as nearest
            .ffill().bfill().drop_duplicates(),

            # Get SVs
            pd.concat(
                [m.svs[['offset', 'multiplier']].df,
                 pd.DataFrame(
                     {'offset': [offset_min, offset_max],
                      'multiplier': [1, 1]}
                 )], ignore_index=True
            )
            .drop_duplicates(),

            # Outer Join on SV and BPM
            on='offset', how='outer'
        )
        # Make sure to sort offset before filling
        .sort_values('offset')
        # Fill in gaps made by OUTER JOIN
        .ffill().bfill()
        # Calculate intervals
        .assign(
            interval=lambda x: x.offset.diff().shift(-1)
        )
    )
    # Find most common BPM
    df_bpm = df_.groupby('bpm').sum().reset_index()
    bpm = df_bpm.iloc[df_bpm.interval.argmax()].bpm

    # Evaluate Speed
    return df_.assign(
        # We take the bpm x sv for the final speed
        speed=lambda x: x.bpm / bpm * x.multiplier,
    )['speed']


# # # We'll evaluate the visual complexity given by the function above.
# # vc=lambda x: visual_complexity(x.speed),
# # # Weight the Visual Complexity Index by the Proportional Interval
# # # We weight by the proportion, so the output range is [0, 1]
# # w_vc=lambda x: x.vc * x.interval / x.interval.sum()
# def visual_complexity(s):
#     # Formula
#     # \left\{x\ge0:\frac{3}{4}\left(xe^{1-x}+0.5\right)^{-1}-\frac{1}{2}\right\}
#     return 3 / 4 * (s * np.exp(1 - s) + 0.5) ** -1 - 1 / 2

from typing import List, Union
import numpy as np
import pandas as pd

from reamber.base import RAConst


class Measure:
    """ For each measure, we have a specified number of Bars.

    Usually, it's 4/4, then we have 4 bars.

    However, if it's 9/4, then it's 9 bars.

    The denominator isn't too useful since it's describing musical length duration.

    The major assumption is that, for measure-based engines, the bars are always complete
    and never half.

    The structure of the ndarray is [beat, snap - 1, slot] (Note that indexing starts at 0).
    """

    df: pd.DataFrame
    offset: float

    def __init__(self, offset: float, divisions: List[int], bpms: Union[List[float], float], beats: int = None):
        """

        :param divisions: The divisions the array should have. 1, 2, 3 implies 1/1, 1/2, 1/3
        :param bpms: The bpms of the bars, can be a single value, which will be repeated for number of beats specified
        :param beats: Only used if bpm is a float, otherwise beats is inferred from bpms.
        """
        bpms = [bpms for _ in range(beats)] if isinstance(bpms, float) else bpms
        self._make_slots(offset, divisions, bpms)

    def _make_slots(self, offset: float, divisions: List[int], bpms: List[float]):
        """ Creates a relative np.ndarray of slots that don't repeat

        The higher order snaps are preferred.

        Relative as all of them aren't on actual offsets

        :param divisions: Divisions to include, if [1,2,3], then 1/1, 1/2, 1/3.
        :param bpms: The bpm for each beat.
        :return: ar_offsets, ar_objs
        """

        beat_lengths = RAConst.MIN_TO_MSEC / np.asarray(bpms)

        max_slots = np.max(divisions)
        exclude = np.arange(max_slots)[np.isin(np.arange(1, max_slots + 1), divisions, invert=True)]

        assert max_slots > 0, f"max_slots cannot be less than 0. {max_slots}"

        # Creates the division triangle
        ar_off = np.zeros([max_slots, max_slots])
        for i in range(max_slots):
            ar_off[i, :i + 1] = np.linspace(0, 1, i + 1, endpoint=False)

        # Prunes the repeated slots
        visited = []
        for i in range(max_slots):
            for j in range(max_slots):
                if ar_off[i, j] in visited:
                    ar_off[i, j] = np.nan
                else:
                    visited.append(ar_off[i, j])

        # Excludes any unwanted snaps
        for exc in exclude:
            assert exc > 0, f"Excluded snap cannot be 0 or less, {exclude}"
            ar_off[exc] = np.nan

        ar_off = np.repeat(ar_off[np.newaxis, ...], len(bpms), 0)
        # Scales to beat lengths
        ar_off *= beat_lengths[..., np.newaxis, np.newaxis]
        beat_cumsum = np.roll(np.cumsum(beat_lengths), 1)
        beat_cumsum[0] = 0
        ar_off += beat_cumsum[..., np.newaxis, np.newaxis]

        # Creates the obj ar
        ar_obj = np.empty_like(ar_off, dtype=object)
        ar_obj[:] = np.nan

        ar = np.stack([ar_off, *np.indices(ar_off.shape)])
        df = pd.DataFrame(ar[:, ~np.isnan(ar[0])].T,
                          columns=['offset', 'beat', 'divisor', 'slot'])
        df['object'] = np.nan
        df['offset'] += offset
        self.df = df


from typing import List, Dict, Tuple, Iterable, Union

import numpy as np
import pandas as pd

from reamber.base import RAConst


class Beat:
    """ We assume Beat holds BPM info. """

    slots_obj: np.ndarray
    slots_offset: np.ndarray
    divisions: List[int]
    bpm: float

    def make_slots(self, divisions: List[int]):
        """ Creates an np.ndarray of slots that don't repeat

        The higher order snaps are preferred.

        :param divisions: Divisions to include, if [1,2,3], then 1/1, 1/2, 1/3.
        :return:
        """

        max_slots = np.max(divisions) - 1
        exclude = np.arange(max_slots)[np.isin(np.arange(1, max_slots + 1), divisions, invert=True)]

        assert max_slots > 0, f"max_slots cannot be less than 0. {max_slots}"

        # Creates the division triangle
        ar = np.zeros([max_slots, max_slots])
        for i in range(max_slots):
            ar[i, :i + 1] = np.linspace(0, 1, i + 1, endpoint=False)

        # Prunes the repeated slots
        visited = []
        for i in range(max_slots):
            for j in range(max_slots):
                if ar[i, j] in visited:
                    ar[i, j] = np.nan
                else:
                    visited.append(ar[i, j])

        # Excludes any unwanted snaps
        for exc in exclude:
            assert exc > 0, f"Excluded snap cannot be 0 or less, {exclude}"
            ar[exc] = np.nan

        # Multiplies the beat length to get the actual offset snap
        self.slots_offset = ar * self.beat_length()
        # Creates the obj ar
        self.slots_obj = np.empty_like(ar, dtype=object)
        self.slots_obj[:] = np.nan

    def __init__(self, divisions: List[int], bpm: float):
        self.bpm = bpm
        self.make_slots(divisions=divisions)

    @property
    def shape(self) -> Tuple:
        return self.slots_offset.shape
    
    def __repr__(self):
        return self.slots_offset.__repr__()

    def ix_closest(self, offset:float):
        """ Gets the closest snap and slot index with its error

        :return: Tuple(Divisor, Slot), Error (ms)
        """
        ix = np.unravel_index(np.nanargmin(np.abs(self.slots_offset - offset)), self.shape)
        return ix, offset - self.slots_offset[ix]

    def get_closest(self, offset:float):
        """ Gets the closest snapped object with its error

        :return: Object, Error (ms)
        """
        ix, er = self.ix_closest(offset=offset)
        return self.slots_obj[ix], er



    def __setitem__(self, key, value):
        self.slots_offset.__setitem__(key, value)

    def beat_length(self):
        return RAConst.minToMSec(1 / self.bpm)




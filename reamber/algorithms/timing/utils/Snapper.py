from __future__ import annotations

from bisect import bisect_left
from fractions import Fraction
from typing import Iterable

import numpy as np

from reamber.algorithms.timing.utils.conf import DEFAULT_DIVISIONS


def snap(value: float,
         divisions: Iterable[int] = DEFAULT_DIVISIONS) -> Fraction:
    """Snaps float value to closest division.

    Args:
        value: Value to snap
        divisions: Divisions to accept
    """
    return Snapper(divisions=divisions).snap(value)


class Snapper:
    def __init__(self, divisions: Iterable[int] = DEFAULT_DIVISIONS):
        """Initialize Snapper with defined divisions

        Args:
            divisions: Divisions acceptable when snapping
        """
        divisions = np.asarray(divisions)
        max_slots = max(divisions)

        # Creates the division triangle
        den, num = np.indices([max_slots, max_slots])
        den += 1
        ar = num / den

        ar[np.triu_indices(ar.shape[0], 1)] = np.nan
        ar[1:, 0] = np.nan
        # Prunes the repeated slots
        visited = set()
        for i in range(1, max_slots):
            for j in range(1, i + 1):
                if ar[i, j] in visited:
                    ar[i, j] = np.nan
                else:
                    visited.add(ar[i, j])

        # Add numerator & denominator
        ar = np.stack([ar, num, den])
        ar = ar[:, ~np.isnan(ar[0])].T
        sorter = ar[:, 0].argsort()

        # Add the case for 1/1 so that 0.9999... matches that
        ar = np.vstack([ar[sorter], [1, 1, 1]])

        self.val = ar[:, 0]
        self.num = ar[:, 1]
        self.den = ar[:, 2]

    def snap(self, beat: float) -> Fraction:
        """Snaps beat to nearest division"""
        quo, rem = beat // 1, beat % 1
        ix = bisect_left(self.val, rem)

        # Bisect Left gets the next value
        # E.g. [0, 0.5], bisect_left(ar, 0.0001) = 1, bisect_left(ar, 0) = 0,
        if ix != 0:
            left_diff, right_diff = \
                rem - self.val[ix - 1], self.val[ix] - rem
            if left_diff < right_diff:
                ix -= 1
        return Fraction(int(self.num[ix]), int(self.den[ix])) + Fraction(quo)

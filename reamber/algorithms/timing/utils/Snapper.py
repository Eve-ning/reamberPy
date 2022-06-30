from __future__ import annotations

from fractions import Fraction
from typing import Iterable

import numpy as np

from reamber.algorithms.timing.utils.conf import DEFAULT_DIVISIONS


def snap(value: float,
         divisions: Iterable[int] = DEFAULT_DIVISIONS) -> Fraction:
    """ Snaps float value to closest division.

    Args:
        value: Value to snap
        divisions: Divisions to accept
    """
    return Snapper(divisions=divisions).snap(value)


class Snapper:
    def __init__(self, divisions: Iterable[int] = DEFAULT_DIVISIONS):
        """ Initialize Snapper with defined divisions

        Args:
            divisions: Divisions acceptable when snapping
        """
        divisions = np.asarray(divisions)
        max_slots = max(divisions)

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

        # Add numerator & denominator
        ar = np.stack([ar, *np.indices(ar.shape)])[:, divisions - 1]
        ar = ar[:, ~np.isnan(ar[0])].T

        # Add the case for 1/1 so that 0.9999... matches that
        self.ar = np.vstack([ar, [1, 0, 1]])

    def snap(self, value: float) -> Fraction:
        """ Snaps float value to closest division """
        closest = self.ar[np.argmin(np.abs(self.ar[:, 0] - (value % 1)))]
        return Fraction(int(closest[2]), int(closest[1] + 1)) + \
               Fraction(value // 1)

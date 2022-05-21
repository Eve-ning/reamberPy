from __future__ import annotations

from fractions import Fraction
from typing import Iterable

import numpy as np


class Slotter:
    def __init__(self,
                 divisions: Iterable[int] = (
                     1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 16, 32, 64, 96)):
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

        ar = np.stack([ar, *np.indices(ar.shape)])[:, divisions - 1]
        self.ar = ar[:, ~np.isnan(ar[0])].T

    def slot(self, frac: float):
        closest = self.ar[np.argmin(np.abs(self.ar[:, 0] - frac))]
        return Fraction(int(closest[2]), int(closest[1] + 1))

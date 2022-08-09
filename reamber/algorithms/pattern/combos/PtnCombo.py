from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Callable

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

from reamber.algorithms.pattern.combos._PtnCChordStream import _PtnCChordStream
from reamber.algorithms.pattern.combos._PtnCJack import _PtnCJack


@dataclass
class PtnCombo(_PtnCChordStream,
               _PtnCJack):
    groups: List[np.ndarray] = field(default_factory=lambda: [])

    def combinations(
        self, size=2, make_size2=False,
        chord_filter: Callable[[np.ndarray], bool] = None,
        combo_filter: Callable[[np.ndarray], np.ndarray[bool]] = None,
        type_filter: Callable[[np.ndarray], np.ndarray[bool]] = None
    ) -> List[np.ndarray]:
        """Gets all combinations of n-size groups with filters

        Args:
            size: The size of each combination.
            make_size2: Whether to fold any size > 2 combinations into pairs
            chord_filter: A chord size filter. Can be generated from
                PtnFilterChord.filter
            combo_filter: A combination filter. Can be generated from
                PtnFilterCombo.filter
            type_filter: A type filter. Can be generated from
                PtnFilterType.filter"""

        # Chunks are groups of groups
        chunks = []

        for i, j in zip(
            range(0, len(self.groups) - size + 1),  # [0, Groups - Size]
            range(size, len(self.groups) + 1)  # [Size, Groups]
        ):
            chunk = self.groups[i:j]

            if (
                chord_filter is None or
                chord_filter(np.array([i.shape[0] for i in chunk]))
            ):
                chunks.append(chunk)

        combo_list: List = []

        for chunk in chunks:
            # This gets all combinations of the list of groups in the chunk
            combos = np.asarray(np.meshgrid(*chunk)).T.reshape(-1, size)
            if combo_filter: combos = combos[combo_filter(combos['column'])]
            if type_filter:  combos = combos[type_filter(combos['type'])]

            combo_list.append(combos)

        combo_list = [_ for _ in combo_list if _.size != 0]
        if make_size2:
            return [sliding_window_view(ar, [ar.shape[0], 2]).reshape(-1, 2)
                    for ar in combo_list]
        else:
            return combo_list

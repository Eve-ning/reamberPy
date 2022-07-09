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
        self, size=2, flatten=False, make_size2=False,
        chord_filter: Callable[[np.ndarray], bool] = None,
        combo_filter: Callable[[np.ndarray], np.ndarray[bool]] = None,
        type_filter: Callable[[np.ndarray], np.ndarray[bool]] = None
    ) -> np.ndarray:
        """ Gets all combinations of n-size groups with filters

        Args:
            size: The size of each combination.
            flatten: Whether to flatten into a singular np.ndarray
            make_size2: If flatten, size > 2 combinations can be further
                flattened by compressing the combinations.
                If flatten is False, this has no effect.
            chord_filter: A chord size filter. Can be generated from
                PtnFilterChord.filter
            combo_filter: A combination filter. Can be generated from
                PtnFilterCombo.filter
            type_filter: A type filter. Can be generated from
                PtnFilterType.filter"""

        """ Chunks are groups that are grouped together in size=size.
        
        e.g.
        Size = 2
        Groups 1 2 3 4 5 6 7 8
        Chunk [ 1 | 3 | 5 | 7 ]
                [ 2 | 4 | 6 ]
        
        A Sequence is a the single-note variation of a chunk.
        
        """

        chunks = []

        # <-SIZE-->
        # L       R
        # 0 1 2 3 4 5 ...
        for left_ix, right_ix in zip(
            range(0, len(self.groups) - size + 1),  # [0, Groups - Size]
            range(size, len(self.groups) + 1)  # [Size, Groups]
        ):
            chunk = self.groups[left_ix:right_ix]

            if (
                chord_filter is None or
                chord_filter(np.array([i.shape[0] for i in chunk]))
            ):
                chunks.append([df.to_records(index=False) for df in chunk])

        combo_list: List = []

        for chunk in chunks:
            # This gets all combinations of the list of groups in the chunk
            combos = np.asarray(np.meshgrid(*chunk)).T.reshape(-1, size)
            if combo_filter: combos = combos[combo_filter(combos['column'])]
            if type_filter:  combos = combos[type_filter(combos['type'])]

            combo_list.append(combos)

        if make_size2:
            ar = np.asarray([i for j in combo_list for i in j])
            return sliding_window_view(ar, [ar.shape[0], 2])
        else:
            return np.array([i for j in combo_list for i in j]) \
                if flatten else combo_list

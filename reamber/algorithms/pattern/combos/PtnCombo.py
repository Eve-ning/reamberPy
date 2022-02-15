from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Callable

import numpy as np

from reamber.algorithms.pattern.combos._PtnCChordStream import _PtnCChordStream
from reamber.algorithms.pattern.combos._PtnCJack import _PtnCJack


@dataclass
class PtnCombo(_PtnCChordStream,
               _PtnCJack):
    """ This class aids in finding Combinations of Groups.

    Groups can be generated with Pattern.groups()"""

    groups: List[np.ndarray] = field(default_factory=lambda: [])

    def combinations(self, size=2, flatten=True, make_size2=False,
                     chord_filter: Callable[[np.ndarray], bool] = None,
                     combo_filter: Callable[[np.ndarray], np.ndarray[bool]] = None,
                     type_filter: Callable[[np.ndarray], np.ndarray[bool]] = None) -> np.ndarray:
        """ Gets all possible combinations of each subsequent n-size

        All filters can be found in pattern.filters.PtnFilter. You need to initialize the class with appropriate args
        then pass the .filter function callable to this combination func.

        The filters can be custom-made. Here's how to customize your filter if the provided filters do not work well

        Note: The size may change, so the Callable should accommodate if possible.

        **Chord Filter**

        Input: ndarray of ``({size},)``. Where it tells us the length of each chord.

        e.g. [3, 4, 1] means there is a 3, 4, 1 note chord respectively.

        The filter must take that as an argument and return a boolean, whether to INCLUDE the chord sequence or not.

        **Combo Filter**

        Input: ndarray of ``(x, {size})``. Where each row tells us the column

        e.g. [[1, 3, 2], [3, 1, 0]] means there is both a 1 -> 3 -> 2 and 3 -> 1 -> 0 pattern in the sequence.

        The filter must take this and return an ndarray boolean of ``(x,)``.

        Each boolean will tell if the chord should be INCLUDED or not.

        **Type Filter**

        Input: ndarray of ``(x, {size})``. Where each row tells us the type

        e.g. [[Hit, Hold], [Hold, HoldTail]] means there is both a Hit -> Hold and Hold -> HoldTail pattern in the
        sequence.

        The filter must take this and return an ndarray boolean of ``(x,)``.

        Each boolean will tell if the chord should be INCLUDED or not.

        :param size: The size of each combination.
        :param flatten: Whether to flatten into a singular np.ndarray
        :param make_size2: If flatten, size > 2 combinations can be further flattened by compressing the combinations.
            If flatten is False, this has no effect.
        :param chord_filter: A chord size filter. Can be generated from PtnFilterChord.filter
        :param combo_filter: A combination filter. Can be generated from PtnFilterCombo.filter
        :param type_filter: A type filter. Can be generated from PtnFilterType.filter"""

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
                range(0, len(self.groups) - size),  # [0, Groups - Size]
                range(size, len(self.groups))  # [Size, Groups]
        ):
            chunk = self.groups[left_ix:right_ix]

            if chord_filter is None or \
                    chord_filter(np.asarray([i.shape[0] for i in chunk])):
                chunks.append(chunk)

        dt = np.dtype([*[(f'column{i}', np.int8) for i in range(size)],
                       *[(f'offset{i}', np.float_) for i in range(size)],
                       *[(f'type{i}', object) for i in range(size)]])

        """ We loop through the chunks here, finding all permutations of each chunk
        
        e.g.
        [0 1][3 4] -> [0][3] + [1][3] + [0][4] + [1][4]
        
        Note that this can scale up for size > 2.
        
        e.g.
        [0][1][3 4] -> [0][1][3] + [0][1][4] ---[makeSize2 == True]---> [0][1] + [1][3] + [0][1] + [0][4]
         
        By allowing makeSize2, this algorithm will extract all 2-permutations. 
        
        At this point is where the filter will take place.
        Depending on size specified, the filter argument will differ.
        """
        combo_list: List = []

        for chunk in chunks:

            # This gets all combinations of the list of groups in the chunk
            combos = np.asarray(np.meshgrid(*chunk)).T.reshape(-1, size)

            # This uses the combo filter to remove all unwanted sequences.
            if combo_filter: combos = combos[combo_filter(combos['column'])]
            if type_filter:  combos = combos[type_filter(combos['type'])]

            """ Here we allocated an empty array to drop our data in. """
            np_combo = np.empty(len(combos), dtype=dt)

            for i, combo in enumerate(combos):
                for j, col, offset, type_ in zip(range(size), combo['column'], combo['offset'], combo['type']):
                    np_combo[i][f'column{j}'] = col
                    np_combo[i][f'offset{j}'] = offset
                    np_combo[i][f'type{j}'] = type_

            combo_list.append(np_combo)

        """ Outputs
        
        Let's say we have 4 original groups, size 3. [0][1 2][3][4]
        
        Reviewing how the algorithm is done.
        
        [0][1 2][3][4] --perm-> [0][1][3] + [0][2][3] then [1][3][4] + [2][3][4] 
        
        If not flatten, we'll get all groups raw.
        [[0][1][3], [0][2][3]],[[1][3][4], [2][3][4]]
        <  From [0][1 2][3]  > <  From [1 2][3][4]  >
        
        If flatten
        [0][1][3], [0][2][3], [1][3][4], [2][3][4]
        
        If flatten and makeSize2
        [0][1], [1][3], [0][2], [2][3], [1][3], [3][4], [2][3], [3][4]
        <  [0][1][3]  > <  [0][2][3]  > <  [1][3][4]  > <  [2][3][4]  > 
        
        If not flatten and makeSize2 will just return raw.
        """

        if not make_size2:
            return np.asarray([i for j in combo_list for i in j]) if flatten else combo_list
        else:
            # This will make pairs out of (>2)-size combos by iterating through the combo pairs.
            ar = np.asarray([i for j in combo_list for i in j])

            # Algo not required for size 2.
            if size == 2: return ar

            s = [ar[[f'column{i}', f'column{i + 1}',
                     f'offset{i}', f'offset{i + 1}',
                     f'type{i}', f'type{i + 1}']] for i in range(size - 1)]

            # Numpy doesn't allow hstack if names are inconsistent.
            for i in s[1:]: i.dtype.names = ['column0', 'column1', 'offset0', 'offset1', 'type0', 'type1']
            return np.hstack(s)

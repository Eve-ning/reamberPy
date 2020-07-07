""" Holds multiple PtnGroups """
from __future__ import annotations
from typing import List, Callable, Type
from reamber.base.lists.notes.NoteList import NoteList
from reamber.base.Hold import Hold
import numpy as np


class PtnPkg:
    def __init__(self, cols: List[int], offsets: List[float], types: List[Type]):
        self.dt = np.dtype([('column', np.int8), ('offset', np.float_),
                            ('groupConfidence', np.float_), ('type', object)])

        assert len(cols) == len(offsets) == len(types),\
            f"All lists must be equal in length {len(cols)}, {len(offsets)}, {len(types)}"

        self.data = np.empty(len(cols), dtype=self.dt)

        # noinspection PyTypeChecker
        cols = [i for i, _ in sorted(zip(cols, offsets), key=lambda j: j[1])]
        types = [i for i, _ in sorted(zip(types, offsets), key=lambda j: j[1])]
        offsets.sort()

        self.data['column'] = cols
        self.data['offset'] = offsets
        self.data['type'] = types
        self.data['groupConfidence'] = 1.0

        # self.dt = np.dtype([('column', np.int8), ('offset', np.float_), ('confidence', np.float_)])
        #
        # if lis_ is None:
        #     self.data = np.empty(0, dtype=self.dt)
        #     return
        #
        # self.data = np.empty(lis_.objCount(), dtype=self.dt)
        # # noinspection PyTypeChecker
        # lisCopy = [obj for i in lis_.deepcopy().data().values() for obj in i]
        # lisCopy.sort(key=lambda x: x.offset)
        # self.data['column'] = [i.column for i in lisCopy]
        # self.data['offset'] = [i.offset for i in lisCopy]
        # self.data['confidence'] = 1.0

    @staticmethod
    def fromPkg(nls: List[NoteList]) -> PtnPkg:
        # noinspection PyTypeChecker
        nls = [nl for nl in nls if len(nl) > 0]
        cols = []
        offsets = []
        types = []

        for nl in nls:
            for obj in nl.data():
                cols.append(obj.column)
                offsets.append(obj.offset)
                types.append(type(obj))

                if isinstance(obj, Hold):
                    cols.append(obj.tailColumn())
                    offsets.append(obj.tailOffset())
                    types.append(type(obj._tail))

        return PtnPkg(cols=cols, offsets=offsets, types=types)

    def __len__(self):
        return len(self.data)

    def copy(self):
        return self.data.copy()

    def empty(self, length: int):
        return np.empty(length, dtype=self.dt)

    def group(self, vwindow: float = 50.0, hwindow:None or int = None, avoidJack=True,
              excludeMarked=True) -> List[np.ndarray]:
        """ Groups the package horizontally and vertically, returns a list of groups

        Warning: Having too high of a hwindow can cause overlapping groups.

        Example::

            | 6 7 X 8
            | 3 X 4 5
            | X 1 2 X
            =========

        If our window is too large, the algorithm will group it as [1,2,3,5][4,6,7,8].

        The overlapping [3,4,5] in 2 groups may cause issues in calculation.

        Let's say we want to group with the parameters
        ``vwindow = 0, hwindow = None``::

            [4s]  _5__           _5__           _5__           _5__           _X__
            [3s]  ___4  GROUP 1  ___4  GROUP 2  ___4  GROUP 3  ___X  GROUP 4  ___X
            [2s]  _2_3  ------>  _2_3  ------>  _X_X  ------>  _X_X  ------>  _X_X
            [1s]  ____  [1]      ____  [2,3]    ____  [4]      ____  [5]      ____
            [0s]  1___           X___           X___           X___           X___

            Output: [1][2,3][4][5]

        ``vwindow = 1000, hwindow = None``::

            [4s]  _5__           _5__           _5__           _X__
            [3s]  ___4  GROUP 1  ___4  GROUP 2  ___X  GROUP 3  ___X
            [2s]  _2_3  ------>  _2_3  ------>  _X_X  ------>  _X_X
            [1s]  ____  [1]      ____  [2,3,4]  ____  [5]      ____
            [0s]  1___           X___           X___           X___

            Output: [1][2,3,4][5]

        2, 3 and 4 are grouped together because 4 is within the vwindow of 2;

        ``2.offset + vwindow <= 4.offset``

        ``vwindow = 1000, hwindow = 1``::

            [4s]  _5__           _5__          _5__           _5__           _X__
            [3s]  ___4  GROUP 1  ___4  GROUP 2 ___4  GROUP 3  ___X  GROUP 4  ___X
            [2s]  _2_3  ------>  _2_3  ------> _X_3  ------>  _X_X  ------>  _X_X
            [1s]  ____  [1]      ____  [2]     ____  [3,4]    ____  [5]      ____
            [0s]  1___           X___          X___           X___           X___

            Output: [1][2][3,4][5]

        2 and 3 aren't grouped together because they are > 1 column apart. (Hence the hwindow argument)

        :param vwindow: The Vertical Window to check (Offsets)
        :param hwindow: The Horizontal Window to check (Columns). If none, all columns will be grouped.
        :param avoidJack: If True, a group will never have duplicate columns.
        :param excludeMarked: If True, any note that is already grouped will never be grouped again. If False, notes\
            that aren't grouped will be used as reference points and may include marked objects.
        """
        assert vwindow >= 0, "VWindow cannot be negative"
        assert hwindow is None or hwindow >= 0, "HWindow cannot be negative, use None to group all columns available."

        groupedArr = np.zeros(len(self), dtype=np.bool_)

        grps = []

        for i, note in enumerate(self.data):
            if groupedArr[i] is np.True_: continue  # Skip all grouped

            mask = np.ones(len(self.data), np.bool_)

            if vwindow >= 0:
                # e.g. searchsorted([0,1,2,6,7,9], 3) -> 2
                # From this we can find the indexes where the groups are.
                left = np.searchsorted(self.data['offset'], note['offset'], side='left')
                right = np.searchsorted(self.data['offset'], note['offset'] + vwindow, side='right')
                vmask = np.zeros(len(self.data), np.bool_)
                indexes = list(range(left, right))

                if avoidJack:
                    # The r-hand checks if in the left-right range, if the column mismatches.
                    # We only want mismatched columns if we avoid jack
                    # e.g. [0, 1, 2]
                    cols = self.data['column'][indexes]

                    unqCols = np.unique(cols)
                    # This finds the first occurrences of each unique column, we add left because it's relative
                    indexes = np.intersect1d(np.array([np.where(cols == col)[0][0] for col in unqCols]) + left,
                                             indexes)
                else:
                    vmask[left:right] = True
                #
                # if True:
                #     indexes = np.intersect1d(np.array(np.where(data['offset'][left:right] != note['offset'])) + left,
                #                              indexes)
                #     indexes = np.append(left, indexes)
                vmask[indexes] = True
                mask = np.bitwise_and(mask, vmask)

            # Filter hwindow
            if hwindow is not None:
                hmask = np.zeros(len(self.data), np.bool_)
                hmask[abs(note['column'] - self.data['column']) <= hwindow] = 1
                mask = np.bitwise_and(mask, hmask)

            if excludeMarked:
                mask = np.bitwise_and(~groupedArr, mask)

            # Depending on if we want to repeat h selections, we mark differently.
            groupedArr = np.bitwise_or(groupedArr, mask)

            conf = list(1 - (self.data[mask]['offset'] - note['offset']) / vwindow)
            data = self.data[mask].copy()
            data['groupConfidence'] = conf
            grps.append(data)

        return grps

    @staticmethod
    def combinations(groups, size=2, flatten=True, makeSize2=False,
                     chordFilter: Callable[[List[int]], bool] = lambda x: True,
                     comboFilter: Callable[[List[int]], bool] = lambda x: True):
        """ Gets all possible combinations of each subsequent n-size

        :param groups: Groups grabbed from .groups()
        :param size: The size of each combination.
        :param flatten: Whether to flatten into a singular np.ndarray
        :param makeSize2: If flatten, size > 2 combinations can be further flattened by compressing the combinations.
        :param chordFilter: A chord size filter. \
            e.g. lambda x: x == [2,1] will only allow groups that are len of 2 then 1 to be parsed.
        :param comboFilter: A combination filter. \
            e.g. lambda x: x == [2,1] will produce combinations that are column 2 then 1.
        :return:
        """

        chunks = []
        groupLen = len(groups)
        for left, right in zip(range(0, groupLen - size), range(size, groupLen)):
            chunk = groups[left:right]

            # Filters out invalid chords
            if chordFilter([len(i) for i in chunk]):
                chunks.append(chunk)

        dt = np.dtype([*[(f'column{i}', np.int8) for i in range(size)],
                       *[(f'offset{i}', np.float_) for i in range(size)],
                       *[(f'type{i}', object) for i in range(size)]])
        comboList: List = []

        for chunk in chunks:
            combos = np.array(np.meshgrid(*chunk)).T.reshape(-1, size)

            combos = combos[np.array([np.logical_or.reduce(comboFilter(combo['column'])) for combo in combos])]
            npCombo = np.empty(len(combos), dtype=dt)

            for i, combo in enumerate(combos):
                diffs = np.diff(combo['offset'])
                for j, col, offset, type_ in zip(range(size), combo['column'], combo['offset'], combo['type']):
                    npCombo[i][f'column{j}'] = col
                    npCombo[i][f'offset{j}'] = offset
                    npCombo[i][f'type{j}'] = type_

            comboList.append(npCombo)

        if not makeSize2:
            return np.asarray([i for j in comboList for i in j]) if flatten else comboList
        else:
            # This will make pairs out of (>2)-size combos by iterating through the combo pairs.
            ar = np.asarray([i for j in comboList for i in j])

            # Algo not required for size 2.
            if size == 2: return ar

            s = [ar[[f'column{i}',f'column{i + 1}',
                     f'offset{i}',f'offset{i + 1}',
                     f'type{i}',  f'type{i + 1}']] for i in range(size - 1)]

            # Numpy doesn't allow hstack if names are inconsistent.
            for i in s[1:]: i.dtype.names = ['column0', 'column1', 'offset0', 'offset1', 'type0', 'type1']
            return np.hstack(s)

    def generateFilterByCount(self, countSeq: List[int], avoidJack: bool = False):


        pass
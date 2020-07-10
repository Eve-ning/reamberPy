from __future__ import annotations
from typing import List, Callable, Type
from reamber.base.lists.notes.NoteList import NoteList
from reamber.base.Hold import Hold
import numpy as np


class Pattern:
    """ This class aids in finding Patterns """

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

    @staticmethod
    def fromPkg(nls: List[NoteList]) -> Pattern:
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
                    # noinspection PyProtectedMember
                    types.append(type(obj._tail))

        return Pattern(cols=cols, offsets=offsets, types=types)

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

            # Within this, we look for objects that fall in the vwindow (+ offset)
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

                vmask[indexes] = True
                mask = np.bitwise_and(mask, vmask)

            # Within this, we look for objects that fall in the hwindow (+ column)
            if hwindow is not None:
                hmask = np.zeros(len(self.data), np.bool_)
                hmask[abs(note['column'] - self.data['column']) <= hwindow] = 1
                mask = np.bitwise_and(mask, hmask)

            # If true, we will never include an object twice
            if excludeMarked:
                mask = np.bitwise_and(~groupedArr, mask)

            # Depending on if we want to repeat h selections, we mark differently.
            groupedArr = np.bitwise_or(groupedArr, mask)

            conf = list(1 - (self.data[mask]['offset'] - note['offset']) / vwindow)
            data = self.data[mask].copy()
            data['groupConfidence'] = conf
            grps.append(data)

        return grps


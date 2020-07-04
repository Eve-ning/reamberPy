""" Holds multiple PtnGroups """
from __future__ import annotations
from reamber.algorithms.pattern.PtnNote import PtnNote
from typing import List
from reamber.base.lists.notes.NoteList import NoteList
from reamber.base.lists.NotePkg import NotePkg
from reamber.algorithms.pattern.PtnGroup import PtnGroup
import numpy as np
from copy import deepcopy


class PtnPkg:
    def __init__(self, lis_:NotePkg):
        self.dt = np.dtype([('column', np.int8), ('offset', np.float_), ('confidence', np.float_)])
        if lis_ is None:
            self.data = np.empty(0, dtype=self.dt)
            return

        self.data = np.empty(lis_.objCount(), dtype=self.dt)
        # noinspection PyTypeChecker
        lisCopy = [obj for i in lis_.deepcopy().data().values() for obj in i]
        lisCopy.sort(key=lambda x: x.offset)
        self.data['column'] = [i.column for i in lisCopy]
        self.data['offset'] = [i.offset for i in lisCopy]
        self.data['confidence'] = 1.0

    def __len__(self):
        return len(self.data)

    def copy(self):
        return self.data.copy()

    def empty(self, length: int):
        return np.empty(length, dtype=self.dt)

    def group(self, vwindow: float = 50.0, hwindow:None or int = None, avoidJack=True,
              excludeMarked=True) -> List[np.ndarray]:
        """ Groups the package horizontally and vertically, returns a list of groups

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

            data = self.data
            mask = np.ones(len(data), np.bool_)

            if vwindow >= 0:
                # e.g. searchsorted([0,1,2,6,7,9], 3) -> 2
                # From this we can find the indexes where the groups are.
                left = np.searchsorted(data['offset'], note['offset'], side='left')
                right = np.searchsorted(data['offset'], note['offset'] + vwindow, side='right')
                vmask = np.zeros(len(data), np.bool_)
                if avoidJack:
                    # The r-hand checks if in the left-right range, if the column mismatches.
                    # We only want mismatched columns if we avoid jack
                    # e.g. [0, 1, 2]
                    cols = data['column'][left:right]

                    unqCols = np.unique(cols)
                    # This finds the first occurrences of each unique column
                    indCols = np.array([np.where(cols == col)[0][0] for col in unqCols])

                    # Add left, because the where search is relative
                    vmask[indCols+left] = True
                else:
                    vmask[left:right] = True
                mask = np.bitwise_and(mask, vmask)

            # Filter hwindow
            if hwindow is not None:
                hmask = np.zeros(len(data), np.bool_)
                hmask[abs(note['column'] - data['column']) <= hwindow] = 1
                mask = np.bitwise_and(mask, hmask)

            if excludeMarked:
                mask = np.bitwise_and(~groupedArr, mask)

            # Depending on if we want to repeat h selections, we mark differently.
            groupedArr = np.bitwise_or(groupedArr, mask)

            conf = list(1 - (self.data[mask]['offset'] - note['offset']) / vwindow)
            data = self.data[mask].copy()
            data['confidence'] = conf
            grps.append(data)

        return grps


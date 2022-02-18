from __future__ import annotations

from typing import List, Type

import numpy as np

from reamber.base.Hold import Hold, HoldTail
from reamber.base.lists.notes import HoldList
from reamber.base.lists.notes.NoteList import NoteList


class Pattern:
    """ This class aids in finding Patterns """

    def __init__(self,
                 cols: List[int],
                 offsets: List[float],
                 types: List[Type]):
        """ Initializes the Pattern structure """

        # Set the expected structure for each entry
        self.dt = np.dtype(
            [
                ('column', np.int8),
                ('offset', np.float_),
                ('difference', np.float_),
                ('type', object)
            ]
        )

        assert len(cols) == len(offsets) == len(types), \
            f"All lists must be equal in length {len(cols)}, {len(offsets)}, {len(types)}"

        self.data = np.empty(len(cols), dtype=self.dt)

        # noinspection PyTypeChecker
        cols = [i for i, _ in sorted(zip(cols, offsets), key=lambda j: j[1])]
        types = [i for i, _ in sorted(zip(types, offsets), key=lambda j: j[1])]
        offsets.sort()

        self.data['column'] = cols
        self.data['offset'] = offsets
        self.data['type'] = types
        self.data['difference'] = 1.0

    @staticmethod
    def from_note_lists(note_lists: List[NoteList]) -> Pattern:
        """ Creates a Pattern Class from a List of Note Lists

        You can create it from any subclass of a NoteList

        :param note_lists: A List of NoteLists
        :return: A Pattern Class
        """

        note_lists = filter(lambda x: len(x) > 0, note_lists)
        cols: List[int] = []
        offsets: List[float] = []
        types: List[type] = []

        for nl in note_lists:
            count: int = len(nl)

            nl_type: type = type(nl[0])
            nl_cols: List[int] = nl.column.tolist()
            nl_offsets: List[float] = nl.offset.tolist()

            cols.extend(nl_cols)
            offsets.extend(nl_offsets)
            types.extend([nl_type, ] * count)

            if issubclass(nl_type, Hold):
                nl: HoldList
                cols.extend(nl_cols)
                offsets.extend(nl.tail_offset)
                types.extend([HoldTail, ] * count)

        return Pattern(cols=cols, offsets=offsets, types=types)

    def __len__(self):
        return len(self.data)

    def group(self,
              v_window: float = 50.0,
              h_window: None or int = None,
              avoid_jack=True,
              avoid_regroup=True) -> List[np.ndarray]:
        """ Groups the package horizontally and vertically, returns a list of groups

        Warning: Having too high of a vwindow can cause overlapping groups.

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

        :param v_window: The Vertical Window to check (Offsets)
        :param h_window: The Horizontal Window to check (Columns). If none, all columns will be grouped.
        :param avoid_jack: If True, a group will never have duplicate columns.
        :param avoid_regroup: Whether already grouped notes should be grouped again. If False, notes not grouped will
            be used as reference points and may include marked objects.
        """

        assert v_window >= 0, \
            "Vertical Window cannot be negative"
        assert h_window is None or h_window >= 0, \
            "Horizontal Window cannot be negative, use None to group all columns available."

        # The objects already in a group
        is_grouped = np.zeros(len(self), dtype=np.bool)
        groups = []

        for i, note in enumerate(self.data):
            if is_grouped[i]: continue  # Skip all children of a group

            offset = note['offset']
            column = note['column']

            group_mask = self.vertical_mask(offset, v_window, avoid_jack)

            if h_window is not None: group_mask &= self.horizontal_mask(column, h_window)

            # If true, we will never include an object twice
            if avoid_regroup: group_mask &= ~is_grouped

            # Mark current group as grouped
            is_grouped |= group_mask

            # group_mask[]
            # Yield group as separate array and calculate confidence
            group = self.data[group_mask].copy()
            group_offset = group['offset']

            confidence = (1 - (group_offset - offset) / v_window).tolist()
            group['difference'] = confidence

            # Add to groups
            groups.append(group)

        return groups

    def vertical_mask(self, offset: int, v_window: float, avoid_jack: bool) -> np.ndarray:
        """ Yields the filtered vertical mask based on offset

        :param offset: The reference offset to scan from
        :param v_window: The size of the scan
        :param avoid_jack: Whether to avoid repeated columns in the mask
        :return: The accepted mask
        """
        offsets = self.data['offset']
        mask = np.zeros(len(self.data), dtype=np.bool)

        # Within this, we look for objects that fall in the vwindow (+ offset)

        # We look for the index of the left and right bounds of the offsets
        # e.g. searchsorted([0,1,2,6,7,9], 3) -> 2

        left = np.searchsorted(offsets, offset, side='left')
        right = np.searchsorted(offsets, offset + v_window, side='right')
        group_ixs: List[int] = list(range(left, right))

        if avoid_jack:
            # To avoid jacks, a column shouldn't appear more than once
            # This simply yields the first occurring column in the group and discards the rest
            # E.g. Group [5, 4, 3, 4, 5]

            # Columns of the current group
            # E.g. [5, 4, 3, 4, 5]
            cols = self.data[group_ixs]['column']
            # E.g. [3, 4, 5]
            unq_cols = np.nonzero(np.bincount(cols))[0]

            # This finds the first occurrences of each unique column, we add left because it's relative
            # E.g. [0, 1, 2]
            group_ixs = np.asarray([np.where(cols == col)[0][0] for col in unq_cols]) + left

        mask[group_ixs] = True
        return mask

    def horizontal_mask(self, column: int, h_window: int) -> np.ndarray:
        """ Yields the filtered horizontal mask based on column

        :param column: Column reference
        :param h_window: Size of horizontal window
        :return:
        """
        # Within this, we look for objects that fall in the hwindow (+ column)
        mask = np.zeros(len(self.data), np.bool)
        # Exclude anything outside
        mask[abs(column - self.data['column']) <= h_window] = True

        return mask

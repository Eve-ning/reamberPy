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
        """ Initializes the Pattern structure

        Examples:
            Note that types are singular types like OsuHit, QuaHold, ...
            Tails must be explicitly HoldTail.

            >>> from reamber.base.Hit import Hit
            ... from reamber.base.Hold import Hold, HoldTail
            ... columns = [0, 1, 1, 2, 2, 3]
            ... offsets = [0, 0, 100, 100, 200, 200]
            ... types = [Hit, Hit, Hit, Hold, HoldTail, Hit]
            ... p = Pattern(columns, offsets, types)

        """

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

        self.ar = np.empty(len(cols), dtype=self.dt)

        # noinspection PyTypeChecker
        cols = [i for i, _ in sorted(zip(cols, offsets), key=lambda j: j[1])]
        types = [i for i, _ in sorted(zip(types, offsets), key=lambda j: j[1])]
        offsets.sort()

        self.ar['column'] = cols
        self.ar['offset'] = offsets
        self.ar['type'] = types
        self.ar['difference'] = 1.0

    @staticmethod
    def from_note_lists(note_lists: List[NoteList]) -> Pattern:
        """ Creates a Pattern Class from a List of Note Lists

        Notes:
            You can create it from any subclass of a NoteList
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

    def group(self,
              v_window: float = 50.0,
              h_window: None or int = None,
              avoid_jack=True,
              avoid_regroup=True) -> List[np.ndarray]:
        """ Groups the package horizontally and vertically

        Notes:
            Having a large vwindow can cause overlapping groups.

        Args:
            v_window: The Vertical Window to check (Offsets)
            h_window: The Horizontal Window to check (Columns).
                If None, all columns will be grouped.
            avoid_jack: If True, a group will never have duplicate columns.
            avoid_regroup: Whether to group notes already grouped again.
                If False, notes not grouped will be used as
                reference points and may include marked objects.
        """

        assert v_window >= 0, \
            "Vertical Window cannot be negative"
        assert h_window is None or h_window >= 0, \
            "Horizontal Window cannot be negative, use None to group all columns available."

        # The objects already in a group
        is_grouped = np.zeros(len(self), dtype=bool)
        groups = []

        for i, note in enumerate(self.ar):
            if is_grouped[i]: continue  # Skip all children of a group

            offset = note['offset']
            column = note['column']

            group_mask = self.v_mask(offset, v_window, avoid_jack)

            if h_window is not None: group_mask &= \
                self.h_mask(column, h_window)

            # If true, we will never include an object twice
            if avoid_regroup: group_mask &= ~is_grouped

            # Mark current group as grouped
            is_grouped |= group_mask

            # group_mask[]
            # Yield group as separate array and calculate confidence
            group = self.ar[group_mask].copy()
            group_offset = group['offset']

            confidence = (1 - (group_offset - offset) / v_window).tolist()
            group['difference'] = confidence

            # Add to groups
            groups.append(group)

        return groups

    def v_mask(self,
               offset: int,
               v_window: float,
               avoid_jack: bool = True) -> np.ndarray:
        """ Get filtered vertical mask of offset

        Args:
            offset: The reference offset to scan from
            v_window: The size of the scan
            avoid_jack: Whether to avoid repeated columns in the mask
        """
        offsets = self.ar['offset']
        mask = np.zeros(len(self.ar), dtype=bool)

        # Look for obs are in the [offset, offset + vwindow]
        start = np.searchsorted(offsets, offset, side='left')
        end = np.searchsorted(offsets, offset + v_window, side='right')

        if avoid_jack:
            # To avoid jacks, a column appears only once
            # Take 1st occurrence in each column, discard the rest

            cols = self.ar[start:end]['column']
            mask_ixs = np.asarray(
                [np.where(cols == col)[0][0] for col in set(cols)]
            ) + start  # we add start because it's relative
            mask[mask_ixs] = True
        else:
            mask[start:end] = True
        return mask

    def h_mask(self, column: int, h_window: int) -> np.ndarray:
        """ Get the filtered horizontal mask of column

        Args:
            column: Column reference
            h_window: Size of horizontal window
        """

        mask = np.zeros(len(self.ar), bool)
        mask[abs(column - self.ar['column']) <= h_window] = True

        return mask

    def __len__(self):
        return len(self.ar)

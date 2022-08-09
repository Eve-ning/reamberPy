from __future__ import annotations

from bisect import bisect_left, bisect_right
from typing import List, Type

import numpy as np
import pandas as pd

from reamber.base.Hold import Hold, HoldTail
from reamber.base.lists.notes import HoldList
from reamber.base.lists.notes.NoteList import NoteList


class Pattern:
    def __init__(self,
                 cols: List[int],
                 offsets: List[float],
                 types: List[Type]):
        """Initializes the Pattern structure

        Examples:

            ``type`` is a singular object type like ``OsuHit``, ``QuaHold``.

            The end of an LN must be ``HoldTail``.

            >>> from reamber.base.Hit import Hit
            ... from reamber.base.Hold import Hold, HoldTail
            ... columns = [0, 1, 1, 2, 2, 3]
            ... offsets = [0, 0, 100, 100, 200, 200]
            ... types = [Hit, Hit, Hit, Hold, HoldTail, Hit]
            ... p = Pattern(columns, offsets, types)
        """

        self.df = pd.DataFrame(
            {'column': cols, 'offset': offsets, 'type': types}
        ).sort_values('offset', ignore_index=True)

    @staticmethod
    def from_note_lists(note_lists: List[NoteList],
                        include_tails: bool = True) -> Pattern:
        """Creates a Pattern Class from a List of Note Lists

        Args:
            note_lists: Note Lists to add, E.g. QuaHitList, BMSHoldList
            include_tails: Whether to include tails in pattern discovery

        Notes:
            You can create it from any subclass of a NoteList,

        Examples:
            >>> from reamber.osu.OsuMap import OsuMap
            >>> m = OsuMap.read_file(...)
            >>> p = Pattern.from_note_lists([m.hits, m.holds])
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

            if include_tails and issubclass(nl_type, Hold):
                nl: HoldList
                cols.extend(nl_cols)
                offsets.extend(nl.tail_offset)
                types.extend([HoldTail, ] * count)

        return Pattern(cols=cols, offsets=offsets, types=types)

    def __len__(self):
        return len(self.df)

    def group(self,
              v_window: float = 50.0,
              h_window: None | int = None,
              avoid_jack=True) -> List[np.ndarray]:
        """Groups the package horizontally and vertically

        Notes:
            Having a large v_window causes overlapping groups.

        Args:
            v_window: Vertical Window to check (Offsets)
            h_window: Horizontal Window to check (Columns).
                If None, all columns will be grouped.
            avoid_jack: Whether a group can have duplicate columns.
        """

        if v_window < 0:
            raise ValueError("Vertical Window cannot be negative")

        if h_window is not None and h_window < 0:
            raise ValueError("Horizontal Window cannot be negative, "
                             "use None to group all columns.")

        # The objects already in a group
        is_grouped = np.zeros(len(self), dtype=bool)
        df_groups = []

        ar = self.df.to_records(index=False)

        for ix, col, offset, *_ in self.df.itertuples():
            if is_grouped[ix]: continue  # Skip all children of a group

            ar_ungrouped = ar[~is_grouped]
            mask = self.v_mask(ar_ungrouped, offset, v_window, avoid_jack)
            if h_window is not None:
                mask &= self.h_mask(ar_ungrouped, col, h_window)

            # Mark current group as grouped
            # Mask is a subset of all False in is_grouped, we select all False
            #  from is_grouped
            is_grouped[~is_grouped] |= mask
            df_groups.append(ar_ungrouped[mask])

        return df_groups

    @staticmethod
    def v_mask(ar: np.ndarray, offset: int, v_window: float,
               avoid_jack: bool) -> np.ndarray:
        """Get filtered vertical mask of offset

        Args:
            ar: np.ndarray to mask
            offset: The reference offset to scan from
            v_window: The size of the scan
            avoid_jack: Whether to avoid repeated columns in the mask
        """
        offsets = ar['offset']
        cols = ar['column'].tolist()
        mask = np.zeros(len(ar), dtype=bool)

        # Look for objects in [offset, offset + v_window]

        start = bisect_left(offsets, offset)
        end = bisect_right(offsets, offset + v_window, lo=start)

        if start != end:
            if avoid_jack:
                # To avoid jacks, a column appears only once
                # Take 1st occurrence and discard the rest
                cols_ = cols[start:end]
                mask_ixs = np.array([cols_.index(i) for i in set(cols_)]) \
                           + start
                mask[mask_ixs] = True
            else:
                mask[start:end] = True
        return mask

    @staticmethod
    def h_mask(ar: np.ndarray, column: int, h_window: int) -> np.ndarray:
        """Get the filtered horizontal mask of column

        Args:
            ar: np.ndarray to mask
            column: Column reference
            h_window: Size of horizontal window
        """

        mask = np.zeros(len(ar), bool)
        mask[abs(column - ar['column']) <= h_window] = True

        return mask

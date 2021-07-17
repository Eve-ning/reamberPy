from __future__ import annotations

import warnings
from typing import Tuple, TypeVar

import pandas as pd

from reamber.base.Hold import Hold
from reamber.base.Property import list_props
from reamber.base.lists.notes.NoteList import NoteList

Item = TypeVar('Item', bound=Hold)

@list_props(Hold)
class HoldList(NoteList[Item]):

    def last_offset(self) -> float:
        """ Get Last Note Offset. This includes the tail """
        return max(self.offset + self.length)

    def first_last_offset(self) -> Tuple[float, float]:
        """ Get First and Last Note Offset. This includes the tail """
        return self.first_offset(), self.last_offset()

    @property
    def head_offset(self) -> pd.Series:
        """ This is an alias to self.offsets """
        return self.offset

    @property
    def tail_offset(self) -> pd.Series:
        """ This gets all the tail offsets by adding the offset to the length. """
        return self.offset + self.length

    def after(self,
              offset: float,
              include_end : bool = False,
              include_tail: bool = False) -> HoldList:
        """ Trims the list to after specified offset

        This assumes that the length > 0. If negative length are present then this will not work.

        If the long note is partially within the bounds, include tail will keep it.

        E.g.       Trim <-----------
                     [--+--]
                        <-----------

        Include Tail: Keeps

        Exclude Tail: Discards

        :param offset: The lower bound in milliseconds
        :param include_end: Whether to include the end
        :param include_tail: Whether to include tail
        :return: Returns a modified copy if not inplace
        """
        if any(self.length < 0) and include_tail:
            warnings.warn("after with include_tail does not work properly for negative length. "
                          "Open a separate Issue for support.")

        if include_end:
            # noinspection PyTypeChecker
            return self[self.offset + (self.length if include_tail else 0) >= offset]
        else:
            # noinspection PyTypeChecker
            return self[self.offset + (self.length if include_tail else 0) > offset]

    def before(self,
              offset: float,
              include_end : bool = False,
              include_head: bool = True) -> HoldList:
        """ Trims the list to after specified offset

        This assumes that the length > 0. If negative length are present then this will not work.

        If the long note is partially within the bounds, include head will keep it.

        E.g. -----------> Trim
                     [--+--]
             ----------->

        Include Head: Keeps

        Exclude Head: Discards

        :param offset: The lower bound in milliseconds
        :param include_end: Whether to include the end
        :param include_head: Whether to include head
        :return: Returns a modified copy if not inplace
        """
        if any(self.length < 0) and not include_head:
            warnings.warn("before without include_head does not work properly for negative length. "
                          "Open a separate Issue for support.")

        if include_end:
            # noinspection PyTypeChecker
            return self[self.offset + (self.length if not include_head else 0) <= offset]
        else:
            # noinspection PyTypeChecker
            return self[self.offset + (self.length if not include_head else 0) < offset]

    def between(self,
                lower_bound: float,
                upper_bound: float,
                include_ends: Tuple[bool, bool] = (True, False),
                include_head: bool = True,
                include_tail: bool = False) -> HoldList:
        return self.after(lower_bound, include_end=include_ends[0], include_tail=include_tail)\
                   .before(upper_bound, include_end=include_ends[1], include_head=include_head)

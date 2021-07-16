from __future__ import annotations

import warnings
from typing import List, Tuple, Union, overload, Any, TypeVar

import pandas as pd

from reamber.base import Hold
from reamber.base.lists.notes.NoteList import NoteList

Item = TypeVar('Item', bound=Hold)

class HoldList(NoteList[Item]):

    @property
    def _init_empty(self) -> dict:
        """ Initializes the DataFrame if no objects are passed to init. """
        return dict(**super(HoldList, self)._init_empty,
                    length=pd.Series([], dtype='float'))


    @property
    def lengths(self) -> Union[pd.Series, Any]:
        return self.df['length']

    @lengths.setter
    def lengths(self, val):
        self.df['length'] = val

    def last_offset(self) -> float:
        """ Get Last Note Offset. This includes the tail """
        return max(self.offsets + self.lengths)

    def first_last_offset(self) -> Tuple[float, float]:
        """ Get First and Last Note Offset. This includes the tail """
        return self.first_offset(), self.last_offset()

    @property
    def head_offsets(self) -> pd.Series:
        """ This is an alias to self.offsets """
        return self.offsets

    @property
    def tail_offsets(self) -> pd.Series:
        """ This gets all the tail offsets by adding the offset to the length. """
        return self.offsets + self.lengths

    def after(self,
              offset: float,
              include_end : bool = False,
              include_tail: bool = False) -> HoldList:
        """ Trims the list to after specified offset

        This assumes that the length > 0. If negative lengths are present then this will not work.

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
        if any(self.lengths < 0) and include_tail:
            warnings.warn("after with include_tail does not work properly for negative lengths. "
                          "Open a separate Issue for support.")

        # noinspection PyTypeChecker
        if include_end:
            return self[self.offsets + (self.lengths if include_tail else 0) >= offset]
        else:
            return self[self.offsets + (self.lengths if include_tail else 0) > offset]

    def before(self,
              offset: float,
              include_end : bool = False,
              include_head: bool = True) -> HoldList:
        """ Trims the list to after specified offset

        This assumes that the length > 0. If negative lengths are present then this will not work.

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
        if any(self.lengths < 0) and not include_head:
            warnings.warn("before without include_head does not work properly for negative lengths. "
                          "Open a separate Issue for support.")

        # noinspection PyTypeChecker
        if include_end:
            return self[self.offsets + (self.lengths if not include_head else 0) <= offset]
        else:
            return self[self.offsets + (self.lengths if not include_head else 0) < offset]

    def between(self,
                lower_bound: float,
                upper_bound: float,
                include_ends: Tuple[bool, bool] = (True, False),
                include_head: bool = True,
                include_tail: bool = False) -> HoldList:
        return self.after(lower_bound, include_end=include_ends[0], include_tail=include_tail)\
                   .before(upper_bound, include_end=include_ends[1], include_head=include_head)

    @property
    def _item_class(self) -> type:
        """ Though this is covered by Generics, the test will fail if it needs to initialize
        with the Generic. """
        return Hold
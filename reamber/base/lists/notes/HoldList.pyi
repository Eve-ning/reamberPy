from __future__ import annotations

from typing import Tuple, Union, Any

import pandas as pd

from reamber.base import Hold
from reamber.base.lists.notes.NoteList import NoteList


class HoldList(NoteList[Hold]):

    @staticmethod
    def _default() -> dict: ...

    @property
    def length(self) -> Union[pd.Series, Any]: ...

    @length.setter
    def length(self, val): ...

    def last_offset(self) -> float: ...

    def first_last_offset(self) -> Tuple[float, float]: ...

    @property
    def head_offset(self) -> pd.Series: ...

    @property
    def tail_offset(self) -> pd.Series: ...

    def after(self, offset: float, include_end: bool = False,
              include_tail: bool = False) -> HoldList: ...

    def before(self, offset: float, include_end: bool = False,
               include_head: bool = True) -> HoldList: ...

    def between(self, lower_bound: float, upper_bound: float,
                include_ends: Tuple[bool, bool] = (True, False),
                include_head: bool = True,
                include_tail: bool = False) -> HoldList: ...

    @property
    def _item_class(self) -> type: ...

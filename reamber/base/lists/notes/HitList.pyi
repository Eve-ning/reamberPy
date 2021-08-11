from __future__ import annotations

from typing import List, Union, overload, Any

import pandas as pd

from reamber.base.Hit import Hit
from reamber.base.lists.notes.NoteList import NoteList



class HitList(NoteList[Hit]):

    def __init__(self, objs: Union[List[Hit], Hit, pd.DataFrame]): ...

    @property
    def _item_class(self) -> type: ...

    @overload
    def __getitem__(self, item: slice) -> HitList: ...
    @overload
    def __getitem__(self, item: list) -> HitList: ...
    @overload
    def __getitem__(self, item: Any) -> HitList: ...
    @overload
    def __getitem__(self, item: int) -> Hit: ...

from __future__ import annotations

from typing import List, Union, overload, Any, TypeVar

import pandas as pd

from reamber.base.Hit import Hit
from reamber.base.Property import list_props
from reamber.base.lists.notes.NoteList import NoteList

Item = TypeVar('Item')


@list_props(Hit)
class HitList(NoteList[Item]):

    def __init__(self, objs: Union[List[Hit], Hit, pd.DataFrame]):
        super().__init__(objs=objs)

    @overload
    def __getitem__(self, item: slice) -> HitList: ...

    @overload
    def __getitem__(self, item: list) -> HitList: ...

    @overload
    def __getitem__(self, item: Any) -> HitList: ...

    @overload
    def __getitem__(self, item: int) -> Hit: ...

    def __getitem__(self, item):
        return super().__getitem__(item)

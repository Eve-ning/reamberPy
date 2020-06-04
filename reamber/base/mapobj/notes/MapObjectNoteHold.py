from __future__ import annotations
from typing import List, Tuple
from reamber.base.HoldObject import HoldObject
from reamber.base.mapobj.notes.MapObjectNoteBase import MapObjectNoteBase


class MapObjectNoteHold(List[HoldObject], MapObjectNoteBase):

    def data(self) -> List[HoldObject]:
        return self

    def lastOffset(self) -> float:
        """ Get Last Note Offset """
        return self.sorted()[-1].tailOffset()

    def firstLastOffset(self) -> Tuple[float, float]:
        """ Get First and Last Note Offset
        This is slightly faster than separately calling the singular functions since it sorts once only
        """
        hos = self.sorted()
        return hos[0].offset, hos[-1].tailOffset()


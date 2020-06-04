from reamber.base.mapobj.notes.MapObjectNoteBase import MapObjectNoteBase
from typing import List, Type
from abc import ABC


class SMMapObjectNoteBase(MapObjectNoteBase, ABC):
    def data(self) -> List[Type]: pass


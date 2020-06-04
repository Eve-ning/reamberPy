from reamber.base.mapobj.notes.MapObjectNoteBase import MapObjectNoteBase
from typing import List, Type
from abc import ABC

from reamber.quaver.QuaNoteObjectMeta import QuaNoteObjectMeta


class QuaMapObjectNoteBase(MapObjectNoteBase, ABC):
    def data(self) -> List[Type[QuaNoteObjectMeta]]: pass

    def keySoundsList(self):
        return self.attributes('keySounds')

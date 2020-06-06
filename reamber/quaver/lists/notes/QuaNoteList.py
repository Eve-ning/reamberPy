from reamber.base.lists.notes.NoteList import NoteList
from typing import List, Type
from abc import ABC

from reamber.quaver.QuaNoteObjMeta import QuaNoteObjMeta


class QuaNoteList(NoteList, ABC):
    def data(self) -> List[Type[QuaNoteObjMeta]]: pass

    def keySoundsList(self):
        return self.attributes('keySounds')

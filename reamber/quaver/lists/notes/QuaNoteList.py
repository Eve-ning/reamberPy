from reamber.base.lists.notes.NoteList import NoteList
from typing import List, Type
from abc import ABC

from reamber.quaver.QuaNoteObjectMeta import QuaNoteObjectMeta


class QuaNoteList(NoteList, ABC):
    def data(self) -> List[Type[QuaNoteObjectMeta]]: pass

    def keySoundsList(self):
        return self.attributes('keySounds')

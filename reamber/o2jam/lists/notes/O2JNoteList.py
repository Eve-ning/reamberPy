from reamber.base.lists.notes.NoteList import NoteList
from typing import List, Type
from abc import ABC

from reamber.o2jam.O2JNoteObjMeta import O2JNoteObjMeta


class O2JNoteList(NoteList, ABC):
    def data(self) -> List[Type[O2JNoteObjMeta]]: pass

    # def volumes(self) -> List[float]:
    #     return self.attribute('volume')
    #
    # def hitsoundFiles(self) -> List[str]:
    #     return self.attribute('hitsoundFile')

from reamber.base.lists.notes.NoteList import NoteList
from typing import List, Type
from abc import ABC

from reamber.o2jam.O2JNoteMeta import O2JNoteMeta


class O2JNoteList(NoteList, ABC):
    def data(self) -> List[Type[O2JNoteMeta]]: pass

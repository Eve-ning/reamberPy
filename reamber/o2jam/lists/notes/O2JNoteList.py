from abc import ABC
from typing import List, Type

from reamber.base.lists.notes.NoteList import NoteList
from reamber.o2jam.O2JNoteMeta import O2JNoteMeta


class O2JNoteList(NoteList, ABC):
    def data(self) -> List[Type[O2JNoteMeta]]: pass

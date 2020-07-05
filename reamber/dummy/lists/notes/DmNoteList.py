from reamber.base.lists.notes.NoteList import NoteList
from typing import List, Type
from abc import ABC


class DmNoteList(NoteList, ABC):
    def data(self) -> List[Type]: pass


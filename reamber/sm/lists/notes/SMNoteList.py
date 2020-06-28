from reamber.base.lists.notes.NoteList import NoteList
from reamber.base.NoteObj import NoteObj
from typing import List
from abc import ABC


class SMNoteList(NoteList, ABC):
    def data(self) -> List[NoteObj]: pass


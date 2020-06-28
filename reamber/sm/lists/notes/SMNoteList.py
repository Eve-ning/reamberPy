from reamber.base.lists.notes.NoteList import NoteList
from reamber.base.Note import Note
from typing import List
from abc import ABC


class SMNoteList(NoteList, ABC):
    def data(self) -> List[Note]: pass


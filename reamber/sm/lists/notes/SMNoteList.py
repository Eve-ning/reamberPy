from abc import ABC
from typing import List

from reamber.base.Note import Note
from reamber.base.lists.notes.NoteList import NoteList


class SMNoteList(NoteList, ABC):
    def data(self) -> List[Note]: pass


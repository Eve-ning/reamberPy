from abc import ABC
from typing import List, Type

from reamber.base.lists.notes.NoteList import NoteList


class BMSNoteList(NoteList, ABC):
    def data(self) -> List[Type]: pass


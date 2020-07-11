from abc import ABC
from typing import List, Type

from reamber.base.lists.notes.NoteList import NoteList


class DmNoteList(NoteList, ABC):
    def data(self) -> List[Type]: pass


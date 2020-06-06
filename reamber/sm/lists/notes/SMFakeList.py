from reamber.sm.lists.notes.SMNoteList import SMNoteList
from reamber.sm.SMFakeObject import SMFakeObject
from typing import List


class SMFakeList(List[SMFakeObject], SMNoteList):
    def data(self) -> List[SMFakeObject]:
        return self

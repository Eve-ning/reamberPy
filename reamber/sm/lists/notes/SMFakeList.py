from reamber.sm.lists.notes.SMNoteList import SMNoteList
from reamber.sm.SMFakeObj import SMFakeObj
from typing import List


class SMFakeList(List[SMFakeObj], SMNoteList):
    def data(self) -> List[SMFakeObj]:
        return self

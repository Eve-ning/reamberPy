from reamber.sm.lists.notes.SMNoteList import SMNoteList
from reamber.sm.SMHitObj import SMHitObj
from typing import List


class SMHitList(List[SMHitObj], SMNoteList):
    def data(self) -> List[SMHitObj]:
        return self

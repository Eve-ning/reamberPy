from reamber.sm.lists.notes.SMNoteList import SMNoteList
from reamber.sm.SMLiftObj import SMLiftObj
from typing import List


class SMLiftList(List[SMLiftObj], SMNoteList):
    def data(self) -> List[SMLiftObj]:
        return self

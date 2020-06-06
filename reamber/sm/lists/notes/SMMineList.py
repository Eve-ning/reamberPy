from reamber.sm.lists.notes.SMNoteList import SMNoteList
from reamber.sm.SMMineObj import SMMineObj
from typing import List


class SMMineList(List[SMMineObj], SMNoteList):
    def data(self) -> List[SMMineObj]:
        return self

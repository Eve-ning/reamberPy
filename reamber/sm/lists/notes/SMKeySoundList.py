from reamber.sm.lists.notes.SMNoteList import SMNoteList
from reamber.sm.SMKeySoundObj import SMKeySoundObj
from typing import List


class SMKeySoundList(List[SMKeySoundObj], SMNoteList):

    def _upcast(self, objList: List = None):
        return SMKeySoundList(objList)

    def data(self) -> List[SMKeySoundObj]:
        return self

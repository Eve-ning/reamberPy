from reamber.o2jam.lists.notes.O2JNoteList import O2JNoteList
from reamber.o2jam.O2JHitObj import O2JHitObj
from typing import List


class O2JHitList(List[O2JHitObj], O2JNoteList):

    def _upcast(self, objList: List = None):
        return O2JHitList(objList)

    def data(self) -> List[O2JHitObj]:
        return self

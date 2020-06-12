from reamber.o2jam.lists.notes.O2JNoteList import O2JNoteList
from reamber.o2jam.O2JHoldObj import O2JHoldObj
from typing import List


class O2JHoldList(List[O2JHoldObj], O2JNoteList):

    def _upcast(self, objList: List = None):
        return O2JHoldList(objList)

    def data(self) -> List[O2JHoldObj]:
        return self

    def lengths(self) -> List[float]:
        return self.attribute('length')

    def offsets(self):
        return [(obj.offset, obj.tailOffset()) for obj in self.data()]

    def tailOffsets(self) -> List[float]:
        return [obj() for obj in self.attribute('tailOffset')]

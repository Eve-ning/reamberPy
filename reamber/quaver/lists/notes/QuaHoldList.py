from reamber.quaver.lists.notes.QuaNoteList import QuaNoteList
from reamber.quaver.QuaHoldObj import QuaHoldObj
from typing import List


class QuaHoldList(List[QuaHoldObj], QuaNoteList):

    def _upcast(self, objList: List = None):
        return QuaHoldList(objList)

    def data(self) -> List[QuaHoldObj]:
        return self

    def lengths(self) -> List[float]:
        return self.attribute('length')

    def offsets(self, flatten=True):
        if flatten: return [i for j in [(obj.offset, obj.tailOffset()) for obj in self.data()] for i in j]
        return [(obj.offset, obj.tailOffset()) for obj in self.data()]

    def tailOffsets(self) -> List[float]:
        return [obj() for obj in self.attribute('tailOffset')]

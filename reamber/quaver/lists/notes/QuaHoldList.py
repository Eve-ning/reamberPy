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

    def tailOffsets(self) -> List[float]:
        return [obj() for obj in self.attribute('tailOffset')]

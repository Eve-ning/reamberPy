from reamber.quaver.lists.notes.QuaNoteList import QuaNoteList
from reamber.quaver.QuaHitObj import QuaHitObj
from typing import List


class QuaHitList(List[QuaHitObj], QuaNoteList):

    def _upcast(self, objList: List = None):
        return QuaHitList(objList)

    def data(self) -> List[QuaHitObj]:
        return self

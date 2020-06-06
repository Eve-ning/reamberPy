from reamber.quaver.lists.notes.QuaNoteList import QuaNoteList
from reamber.quaver.QuaHitObject import QuaHitObject
from typing import List


class QuaHitList(List[QuaHitObject], QuaNoteList):
    def data(self) -> List[QuaHitObject]:
        return self

from __future__ import annotations
from reamber.quaver.lists.notes.QuaNoteList import QuaNoteList
from reamber.quaver.QuaHitObj import QuaHitObj
from typing import List


class QuaHitList(List[QuaHitObj], QuaNoteList):

    def _upcast(self, objList: List = None) -> QuaHitList:
        """ This is to facilitate inherited functions to work

        :param objList: The List to cast
        :rtype: QuaHitList
        """
        return QuaHitList(objList)

    def data(self) -> List[QuaHitObj]:
        return self

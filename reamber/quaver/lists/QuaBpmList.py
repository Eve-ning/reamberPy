from typing import List

from reamber.base.lists.BpmList import BpmList
from reamber.quaver.QuaBpmObj import QuaBpmObj


class QuaBpmList(BpmList):

    def _upcast(self, objList: List = None):
        return QuaBpmList(objList)

    def data(self) -> List[QuaBpmObj]:
        return self

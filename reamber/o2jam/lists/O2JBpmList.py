from typing import List

from reamber.base.lists.BpmList import BpmList
from reamber.o2jam.O2JBpmObj import O2JBpmObj


class O2JBpmList(BpmList):

    def _upcast(self, objList: List = None):
        return O2JBpmList(objList)

    def data(self) -> List[O2JBpmObj]:
        return self

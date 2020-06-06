from typing import List

from reamber.base.lists.BpmList import BpmList
from reamber.sm.SMBpmObj import SMBpmObj


class SMBpmList(BpmList):

    def _upcast(self, objList: List = None):
        return SMBpmList(objList)

    def data(self) -> List[SMBpmObj]:
        return self

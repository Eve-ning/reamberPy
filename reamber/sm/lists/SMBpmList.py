from typing import List

from reamber.base.lists.BpmList import BpmList
from reamber.sm.SMBpmObject import SMBpmObject


class SMBpmList(BpmList):
    def data(self) -> List[SMBpmObject]:
        return self

from typing import List

from reamber.base.lists.BpmList import BpmList
from reamber.sm.SMBpmObj import SMBpmObj


class SMBpmList(BpmList):
    def data(self) -> List[SMBpmObj]:
        return self

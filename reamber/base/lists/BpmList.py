from typing import List
from reamber.base.BpmObject import BpmObject
from reamber.base.lists.TimedList import TimedList


class BpmList(List[BpmObject], TimedList):

    def data(self) -> List[BpmObject]:
        return self

    def bpms(self) -> List[float]:
        return self.attributes('bpm')

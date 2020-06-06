from typing import List
from reamber.base.BpmObj import BpmObj
from reamber.base.lists.TimedList import TimedList
from abc import ABC


class BpmList(List[BpmObj], TimedList, ABC):

    def data(self) -> List[BpmObj]:
        return self

    def bpms(self) -> List[float]:
        return self.attribute('bpm')

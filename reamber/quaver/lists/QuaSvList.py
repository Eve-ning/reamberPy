from reamber.base.lists.TimedList import TimedList
from reamber.quaver.QuaSvObj import QuaSvObj
from typing import List


class QuaSvList(List[QuaSvObj], TimedList):

    def data(self) -> List[QuaSvObj]:
        return self

    def multipliers(self) -> List[float]:
        return self.attribute('multiplier')

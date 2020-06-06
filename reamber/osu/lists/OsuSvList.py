from reamber.base.lists.TimedList import TimedList
from reamber.osu.OsuSvObj import OsuSvObj
from typing import List


class OsuSvList(List[OsuSvObj], TimedList):

    def data(self) -> List[OsuSvObj]:
        return self

    def multipliers(self) -> List[float]:
        return self.attribute('multiplier')

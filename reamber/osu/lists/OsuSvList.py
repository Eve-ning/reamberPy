from reamber.base.lists.TimedList import TimedList
from reamber.osu.OsuSvObject import OsuSvObject
from typing import List


class OsuSvList(List[OsuSvObject], TimedList):

    def data(self) -> List[OsuSvObject]:
        return self

    def multipliers(self) -> List[float]:
        return self.attributes('multiplier')

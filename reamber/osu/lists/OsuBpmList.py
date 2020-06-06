from typing import List

from reamber.base.lists.BpmList import BpmList
from reamber.osu.OsuBpmObject import OsuBpmObject


class OsuBpmList(BpmList):
    def data(self) -> List[OsuBpmObject]:
        return self

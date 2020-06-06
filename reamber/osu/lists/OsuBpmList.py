from typing import List

from reamber.base.lists.BpmList import BpmList
from reamber.osu.OsuBpmObj import OsuBpmObj


class OsuBpmList(BpmList):
    def data(self) -> List[OsuBpmObj]:
        return self

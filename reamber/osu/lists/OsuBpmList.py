from typing import List

from reamber.base.lists.BpmList import BpmList
from reamber.osu.OsuBpmObj import OsuBpmObj


class OsuBpmList(BpmList):

    def _upcast(self, objList: List = None):
        return OsuBpmList(objList)

    def data(self) -> List[OsuBpmObj]:
        return self

from reamber.base.mapobj.MapObjectGeneric import MapObjectGeneric
from reamber.base.mapobj.MapObjectDataFrame import MapObjectDataFrame
from reamber.osu.OsuSliderVelocity import OsuSliderVelocity
from typing import List


class OsuMapObjectSvs(List[OsuSliderVelocity], MapObjectGeneric, MapObjectDataFrame):

    def __init__(self, *args):
        list.__init__(self, *args)

    def data(self) -> List[OsuSliderVelocity]:
        return self


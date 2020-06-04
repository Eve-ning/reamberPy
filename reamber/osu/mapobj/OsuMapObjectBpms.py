from typing import List

from reamber.base.mapobj.MapObjectBpms import MapObjectBpms
from reamber.osu.OsuBpmPoint import OsuBpmPoint


class OsuMapObjectBpms(MapObjectBpms):
    def data(self) -> List[OsuBpmPoint]:
        return self

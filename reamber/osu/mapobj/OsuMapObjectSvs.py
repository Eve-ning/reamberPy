from reamber.base.mapobj.MapObjectBase import MapObjectBase
from reamber.osu.OsuSliderVelocity import OsuSliderVelocity
from typing import List


class OsuMapObjectSvs(List[OsuSliderVelocity], MapObjectBase):

    def data(self) -> List[OsuSliderVelocity]:
        return self

    def velocities(self) -> List[float]:
        return self.attributes('velocity')

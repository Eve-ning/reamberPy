from reamber.base.mapobj.MapObjectBase import MapObjectBase
from reamber.quaver.QuaSliderVelocity import QuaSliderVelocity
from typing import List


class QuaMapObjectSvs(List[QuaSliderVelocity], MapObjectBase):

    def data(self) -> List[QuaSliderVelocity]:
        return self

    def multipliers(self) -> List[float]:
        return self.attributes('multiplier')

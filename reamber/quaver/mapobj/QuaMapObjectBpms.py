from typing import List

from reamber.base.mapobj.MapObjectBpms import MapObjectBpms
from reamber.quaver.QuaBpmPoint import QuaBpmPoint


class QuaMapObjectBpms(MapObjectBpms):
    def data(self) -> List[QuaBpmPoint]:
        return self

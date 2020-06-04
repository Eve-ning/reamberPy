from typing import List

from reamber.base.mapobj.MapObjectBpms import MapObjectBpms
from reamber.sm.SMBpmPoint import SMBpmPoint


class SMMapObjectBpms(MapObjectBpms):
    def data(self) -> List[SMBpmPoint]:
        return self

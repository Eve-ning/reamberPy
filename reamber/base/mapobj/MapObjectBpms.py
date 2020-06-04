from typing import List
from reamber.base.BpmPoint import BpmPoint
from reamber.base.mapobj.MapObjectBase import MapObjectBase


class MapObjectBpms(List[BpmPoint], MapObjectBase):

    def data(self) -> List[BpmPoint]:
        return self

    def bpms(self) -> List[float]:
        return self.attributes('bpm')

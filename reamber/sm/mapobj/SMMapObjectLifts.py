from reamber.base.mapobj.MapObjectGeneric import MapObjectGeneric
from reamber.base.mapobj.MapObjectDataFrame import MapObjectDataFrame
from reamber.sm.SMLiftObject import SMLiftObject
from typing import List


class SMMapObjectLifts(List[SMLiftObject], MapObjectGeneric, MapObjectDataFrame):

    def __init__(self, *args):
        list.__init__(self, *args)

    def data(self) -> List[SMLiftObject]:
        return self


from reamber.base.mapobj.MapObjectGeneric import MapObjectGeneric
from reamber.base.mapobj.MapObjectDataFrame import MapObjectDataFrame
from reamber.sm.SMMineObject import SMMineObject
from typing import List


class SMMapObjectMines(List[SMMineObject], MapObjectGeneric, MapObjectDataFrame):

    def __init__(self, *args):
        list.__init__(self, *args)

    def data(self) -> List[SMMineObject]:
        return self


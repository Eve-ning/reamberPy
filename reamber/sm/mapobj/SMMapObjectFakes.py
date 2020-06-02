from reamber.base.mapobj.MapObjectGeneric import MapObjectGeneric
from reamber.base.mapobj.MapObjectDataFrame import MapObjectDataFrame
from reamber.sm.SMFakeObject import SMFakeObject
from typing import List


class SMMapObjectFakes(List[SMFakeObject], MapObjectGeneric, MapObjectDataFrame):

    def __init__(self, *args):
        list.__init__(self, *args)

    def data(self) -> List[SMFakeObject]:
        return self


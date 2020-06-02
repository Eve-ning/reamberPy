from reamber.base.mapobj.MapObjectGeneric import MapObjectGeneric
from reamber.base.mapobj.MapObjectDataFrame import MapObjectDataFrame
from reamber.sm.SMKeySoundObject import SMKeySoundObject
from typing import List


class SMMapObjectKeySounds(List[SMKeySoundObject], MapObjectGeneric, MapObjectDataFrame):

    def __init__(self, *args):
        list.__init__(self, *args)

    def data(self) -> List[SMKeySoundObject]:
        return self


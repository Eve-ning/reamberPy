from typing import List
from reamber.base.BpmPoint import BpmPoint
from reamber.base.mapobj.MapObjectGeneric import MapObjectGeneric
from reamber.base.mapobj.MapObjectDataFrame import MapObjectDataFrame
import pandas as pd


class MapObjectBpms(List[BpmPoint], MapObjectGeneric, MapObjectDataFrame):

    def __init__(self, *args):
        list.__init__(self, *args)

    def data(self) -> List[BpmPoint]:
        return self

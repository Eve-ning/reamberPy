from typing import List
from reamber.base.BpmPoint import BpmPoint
import pandas as pd


class MapObjectBpms(List[BpmPoint]):

    def __init__(self, *args):
        list.__init__(self, *args)

    def df(self) -> pd.DataFrame:
        return pd.DataFrame({'noteObjects' : self})

    def sorted(self) -> List[BpmPoint]:
        """ Returns a copy of Sorted BPMs """
        return sorted(self, key=lambda tp: tp.offset)

    def offsets(self, by: float):
        """ Move all bpms by a specific ms """
        for bpm in self: bpm.offset += by
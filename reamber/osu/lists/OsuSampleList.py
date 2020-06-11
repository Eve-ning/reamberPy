from typing import List

from reamber.osu.OsuSampleObj import OsuSampleObj
from reamber.base.lists.TimedList import TimedList


class OsuSampleList(List[OsuSampleObj], TimedList):

    def _upcast(self, objList: List = None):
        return OsuSampleList(objList)

    def data(self) -> List[OsuSampleObj]:
        return self

    def sampleFiles(self) -> List[str]:
        return self.attribute('sampleFile')

    def volumes(self) -> List[int]:
        return self.attribute('volume')

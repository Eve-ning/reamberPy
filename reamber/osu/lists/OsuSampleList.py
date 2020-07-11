from __future__ import annotations

from typing import List

from reamber.base.lists.TimedList import TimedList
from reamber.osu.OsuSample import OsuSample


class OsuSampleList(List[OsuSample], TimedList):

    def _upcast(self, objList: List = None) -> OsuSampleList:
        """ This is to facilitate inherited functions to work

        :param objList: The List to cast
        :rtype: OsuSampleList
        """
        return OsuSampleList(objList)

    def data(self) -> List[OsuSample]:
        return self

    def sampleFiles(self) -> List[str]:
        return self.attribute('sampleFile')

    def volumes(self) -> List[int]:
        return self.attribute('volume')

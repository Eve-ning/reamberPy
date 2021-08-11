from __future__ import annotations

from typing import List

import pandas as pd

from reamber.base.Property import list_props
from reamber.base.lists.TimedList import TimedList
from reamber.osu.OsuSample import OsuSample

@list_props(OsuSample)
class OsuSampleList(TimedList[OsuSample]):

    @staticmethod
    def read(strings: List[str]) -> OsuSampleList:
        """ A shortcut to reading OsuHit in a loop to create a OsuHitList

        :param strings: A List of strings to loop through OsuHit.read
        """
        return OsuSampleList(pd.DataFrame([OsuSample.read_string(s, True) for s in strings]))

    def write(self) -> List[str]:
        return [h.write_string() for h in self]

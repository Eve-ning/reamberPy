from __future__ import annotations

from typing import List

import pandas as pd

from reamber.base.Property import list_props
from reamber.base.lists.TimedList import TimedList
from reamber.osu.OsuSv import OsuSv


@list_props(OsuSv)
class OsuSvList(TimedList[OsuSv]):

    @staticmethod
    def read(strings: List[str]) -> OsuSvList:
        return OsuSvList(pd.DataFrame(
            [OsuSv.read_string(s, as_dict=True) for s in
             strings]) if strings else [])

    def write(self) -> List[str]:
        return [h.write_string() for h in self]

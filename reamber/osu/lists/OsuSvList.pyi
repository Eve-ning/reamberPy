from __future__ import annotations

from typing import List

import pandas as pd

from reamber.base.lists.TimedList import TimedList
from reamber.osu.OsuSv import OsuSv


class OsuSvList(TimedList[OsuSv]):

    @staticmethod
    def read(strings: List[str]) -> OsuSvList: ...

    def write(self) -> List[str]: ...

    @property
    def multiplier(self) -> pd.Series: ...

    @multiplier.setter
    def multiplier(self, val) -> None: ...

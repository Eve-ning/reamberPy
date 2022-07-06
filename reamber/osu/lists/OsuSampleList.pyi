from __future__ import annotations

from typing import List

import pandas as pd

from reamber.base.lists.TimedList import TimedList
from reamber.osu.OsuSample import OsuSample


class OsuSampleList(TimedList[OsuSample]):
    @staticmethod
    def read(strings: List[str]) -> OsuSampleList: ...

    def write(self) -> List[str]: ...

    @property
    def sample_file(self) -> pd.Series: ...

    @sample_file.setter
    def sample_file(self, val) -> None: ...

    @property
    def volume(self) -> pd.Series: ...

    @volume.setter
    def volume(self, val) -> None: ...

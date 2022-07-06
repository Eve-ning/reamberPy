from __future__ import annotations

from typing import List

import pandas as pd

from reamber.base.lists.BpmList import BpmList
from reamber.osu.OsuBpm import OsuBpm


class OsuBpmList(BpmList[OsuBpm]):

    @staticmethod
    def read(strings: List[str]) -> OsuBpmList: ...

    def write(self) -> List[str]: ...

    @property
    def sample_set(self) -> pd.Series: ...

    @sample_set.setter
    def sample_set(self, val) -> None: ...

    @property
    def sample_set_index(self) -> pd.Series: ...

    @sample_set_index.setter
    def sample_set_index(self, val) -> None: ...

    @property
    def volume(self) -> pd.Series: ...

    @volume.setter
    def volume(self, val) -> None: ...

    @property
    def kiai(self) -> pd.Series: ...

    @kiai.setter
    def kiai(self, val) -> None: ...

from __future__ import annotations


import pandas as pd

from reamber.base.Property import list_props
from reamber.base.lists.TimedList import TimedList
from reamber.osu.OsuSample import OsuSample

@list_props(OsuSample)
class OsuSampleList(TimedList[OsuSample]):
    @property
    def sample_file(self) -> pd.Series: ...
    @sample_file.setter
    def sample_file(self, val) -> None: ...

    @property
    def volume(self) -> pd.Series: ...
    @volume.setter
    def volume(self, val) -> None: ...



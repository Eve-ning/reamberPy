from __future__ import annotations

from typing import TypeVar

import pandas as pd

from reamber.algorithms.timing.TimingMap import TimingMap
from reamber.base.lists.TimedList import TimedList

Item = TypeVar('Item')


class BpmList(TimedList[Item]):
    def current_bpm(self, offset: float, sort=True) -> Item: ...

    @property
    def bpm(self) -> pd.Series: ...

    @bpm.setter
    def bpm(self, val): ...

    @property
    def metronome(self): ...

    @metronome.setter
    def metronome(self, val): ...

    def snap_offsets(self, nths: float = 1.0,
                     last_offset: float = None) -> np.ndarray: ...

    def to_timing_map(self) -> TimingMap: ...

    def ave_bpm(self, last_offset: float = None) -> float: ...

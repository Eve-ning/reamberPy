from __future__ import annotations

from typing import List, overload, Any, Union, TypeVar

import numpy as np
import pandas as pd

from reamber.algorithms.timing import TimingMap, BpmChangeOffset
from reamber.base import Bpm
from reamber.base import RAConst
from reamber.base.Property import list_props
from reamber.base.lists.TimedList import TimedList


class BpmList(TimedList[Bpm]):
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


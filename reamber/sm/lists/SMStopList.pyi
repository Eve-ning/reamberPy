from __future__ import annotations

import pandas as pd

from reamber.base.lists.TimedList import TimedList
from reamber.sm import SMStop


class SMStopList(TimedList[SMStop]):
    @property
    def length(self) -> pd.Series: ...

    @length.setter
    def length(self, val) -> None: ...

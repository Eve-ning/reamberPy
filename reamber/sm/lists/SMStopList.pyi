from __future__ import annotations

import pandas as pd

from reamber.base.lists.TimedList import TimedList
from reamber.sm import SMStop


class SMStopList(TimedList[SMStop]):
    @property
    def lengths(self) -> pd.Series: ...
    @lengths.setter
    def lengths(self, val) -> None: ...

from __future__ import annotations

from typing import List, Dict, Any

import pandas as pd

from reamber.base.lists.TimedList import TimedList
from reamber.quaver.QuaSv import QuaSv


class QuaSvList(TimedList[QuaSv]):
    @staticmethod
    def read(dicts: List[Dict[str, Any]]) -> QuaSvList:
    @property
    def multiplier(self) -> pd.Series: ...
    @multiplier.setter
    def multiplier(self, val) -> None: ...

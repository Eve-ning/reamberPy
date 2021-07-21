from __future__ import annotations

from plistlib import Dict
from typing import List, Any

from reamber.base.lists.BpmList import BpmList
from reamber.quaver.QuaBpm import QuaBpm


class QuaBpmList(BpmList[QuaBpm]):
    @staticmethod
    def read(dicts: List[Dict[str, Any]]) -> QuaBpmList: ...

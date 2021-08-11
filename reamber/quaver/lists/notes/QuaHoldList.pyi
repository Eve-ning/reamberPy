from __future__ import annotations

from typing import List, Dict

from reamber.base.lists.notes.HoldList import HoldList
from reamber.quaver.QuaHold import QuaHold
from reamber.quaver.lists.notes.QuaNoteList import QuaNoteList


class QuaHoldList(HoldList[QuaHold], QuaNoteList[QuaHold]):
    @staticmethod
    def from_yaml(dicts: List[Dict[str]]) -> QuaHoldList: ...

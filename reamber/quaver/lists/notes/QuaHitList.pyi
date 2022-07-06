from __future__ import annotations

from typing import List, Dict, Any

from reamber.base.lists.notes.HitList import HitList
from reamber.quaver.QuaHit import QuaHit
from reamber.quaver.lists.notes.QuaNoteList import QuaNoteList


class QuaHitList(HitList[QuaHit], QuaNoteList[QuaHit]):
    @staticmethod
    def from_yaml(dicts: List[Dict[str, Any]]) -> QuaHitList: ...

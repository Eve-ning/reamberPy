from __future__ import annotations

from typing import List, Dict, Any, TypeVar

from reamber.base import Timed
from reamber.base.lists import TimedList

Item = TypeVar('Item', bound=Timed)


class QuaTimedList(TimedList[Item]):
    def to_yaml(self): ...

    @staticmethod
    def from_yaml(dicts: List[Dict[str, Any]]) -> QuaTimedList: ...

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar, List, Dict, Any

import pandas as pd

from reamber.base.lists.notes.NoteList import NoteList
from reamber.quaver.lists import QuaTimedList

Item = TypeVar('Item')

class QuaNoteList(NoteList[Item], QuaTimedList[Item], ABC):
    def to_yaml(self) -> List[Dict[str, Any]]: ...

    @staticmethod
    @abstractmethod
    def from_yaml(dicts: List[Dict[str, Any]]) -> QuaNoteList: ...

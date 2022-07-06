from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar, List, Dict, Any

from reamber.base.Property import list_props
from reamber.base.lists.notes.NoteList import NoteList
from reamber.quaver.QuaHit import QuaHit
from reamber.quaver.lists.QuaTimedList import QuaTimedList

Item = TypeVar('Item', bound=QuaHit)

@list_props(QuaHit)
class QuaNoteList(NoteList[Item], QuaTimedList[Item], ABC):

    @staticmethod
    @abstractmethod
    def from_yaml(dicts: List[Dict[str, Any]]) -> QuaNoteList: ...

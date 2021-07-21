from __future__ import annotations

from abc import ABC
from typing import TypeVar

from reamber.base.Property import list_props
from reamber.base.lists.notes.NoteList import NoteList
from reamber.quaver.QuaHit import QuaHit

Item = TypeVar('Item')

@list_props(QuaHit)
class QuaNoteList(NoteList[Item], ABC):
    ...

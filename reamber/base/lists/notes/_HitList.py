from __future__ import annotations
from typing import List
from reamber.base.HitObj import HitObj
from reamber.base.lists.notes.NoteList import NoteList


class HitList(List[HitObj], NoteList):
    def data(self) -> List[HitObj]:
        return self


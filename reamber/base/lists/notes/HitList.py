from __future__ import annotations
from typing import List
from reamber.base.HitObject import HitObject
from reamber.base.lists.notes.NoteList import NoteList


class HitList(List[HitObject], NoteList):
    def data(self) -> List[HitObject]:
        return self


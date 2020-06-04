from __future__ import annotations
from typing import List
from reamber.base.HitObject import HitObject
from reamber.base.mapobj.notes.MapObjectNoteBase import MapObjectNoteBase


class MapObjectNoteHit(List[HitObject], MapObjectNoteBase):
    def data(self) -> List[HitObject]:
        return self


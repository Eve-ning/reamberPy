from __future__ import annotations
from typing import List
from reamber.base.HitObject import HitObject
from reamber.base.HoldObject import HoldObject
from reamber.base.mapobj.notes.MapObjectNoteHit import MapObjectNoteHit
from reamber.base.mapobj.notes.MapObjectNoteHold import MapObjectNoteHold
from abc import abstractmethod
from typing import TypeVar

HitBase = TypeVar("HitBase", bound=HitObject)
HoldBase = TypeVar("HoldBase", bound=HoldObject)


class MapObjectNotes:

    pass
    # @property
    # @abstractmethod
    # def hits(self) -> HitBase: pass
    #
    # @property
    # @abstractmethod
    # def holds(self) -> HoldBase: pass

    # def __init__(self, notes=None):
    #     if notes is None: notes = []
    #     if isinstance(notes, list):
    #         self.hits  = MapObjectNoteHit( [obj for obj in notes if isinstance(notes, HitObject)])
    #         self.holds = MapObjectNoteHold([obj for obj in notes if isinstance(notes, HoldObject)])
    #     elif isinstance(notes, MapObjectNotes):
    #         self.hits = notes.hits
    #         self.holds = notes.holds
    #
    # def data(self) -> List:
    #     return self.hits.data() + self.holds.data()
    #
    # def offsets(self) -> List[float]:
    #     return self.hits.offsets() + self.holds.offsets()


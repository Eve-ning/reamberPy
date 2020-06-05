from reamber.base.mapobj.MapObjectNotes import MapObjectNotes
from reamber.quaver.mapobj.notes.QuaMapObjectHits import QuaMapObjectHits
from reamber.quaver.mapobj.notes.QuaMapObjectHolds import QuaMapObjectHolds
from dataclasses import dataclass, field
from typing import List


@dataclass
class QuaMapObjectNotes(MapObjectNotes):

    hits: QuaMapObjectHits = field(default_factory=lambda: QuaMapObjectHits())
    holds: QuaMapObjectHolds = field(default_factory=lambda: QuaMapObjectHolds())

    def data(self) -> List:
        # noinspection PyTypeChecker
        return self.hits.data() + self.holds.data()

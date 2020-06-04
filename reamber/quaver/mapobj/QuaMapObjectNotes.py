from reamber.base.mapobj.MapObjectNotes import MapObjectNotes
from reamber.quaver.mapobj.notes.QuaMapObjectHits import QuaMapObjectHits
from reamber.quaver.mapobj.notes.QuaMapObjectHolds import QuaMapObjectHolds
from dataclasses import dataclass, field


@dataclass
class QuaMapObjectNotes(MapObjectNotes):
    hits: QuaMapObjectHits = field(default_factory=lambda: QuaMapObjectHits())
    holds: QuaMapObjectHolds = field(default_factory=lambda: QuaMapObjectHolds())

    def firstOffset(self):
        return min(self.hits.firstOffset(), self.holds.firstOffset())

    def lastOffset(self):
        return max(self.hits.lastOffset(), self.holds.lastOffset())

    def firstLastOffset(self):
        return self.firstOffset(), self.lastOffset()

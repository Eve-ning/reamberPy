from reamber.base.mapobj.MapObjectNotes import MapObjectNotes
from reamber.quaver.mapobj.notes.QuaMapObjectHits import QuaMapObjectHits
from reamber.quaver.mapobj.notes.QuaMapObjectHolds import QuaMapObjectHolds
from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class QuaMapObjectNotes(MapObjectNotes):

    hits: QuaMapObjectHits = field(default_factory=lambda: QuaMapObjectHits())
    holds: QuaMapObjectHolds = field(default_factory=lambda: QuaMapObjectHolds())

    def columns(self) -> List[int]:
        return self.hits.columns() + self.holds.columns()

    def offsets(self) -> List[float]:
        return self.hits.offsets() + self.holds.offsets()

    def data(self) -> List:
        # noinspection PyTypeChecker
        return self.hits.data() + self.holds.data()

    def __len__(self) -> int:
        return len(self.hits) + len(self.holds)

    def __iter__(self):
        yield self.hits
        yield self.holds

    def firstOffset(self) -> float:
        return min(self.hits.firstOffset(), self.holds.firstOffset())

    def lastOffset(self) -> float:
        return max(self.hits.lastOffset(), self.holds.lastOffset())

    def firstLastOffset(self) -> Tuple[float, float]:
        return self.firstOffset(), self.lastOffset()

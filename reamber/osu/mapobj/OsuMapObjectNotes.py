from reamber.base.mapobj.MapObjectNotes import MapObjectNotes
from reamber.osu.mapobj.notes.OsuMapObjectHits import OsuMapObjectHits
from reamber.osu.mapobj.notes.OsuMapObjectHolds import OsuMapObjectHolds
from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class OsuMapObjectNotes(MapObjectNotes):

    hits: OsuMapObjectHits = field(default_factory=lambda: OsuMapObjectHits())
    holds: OsuMapObjectHolds = field(default_factory=lambda: OsuMapObjectHolds())

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




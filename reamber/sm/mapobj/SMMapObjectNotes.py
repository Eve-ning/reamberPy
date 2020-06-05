from reamber.base.mapobj.MapObjectNotes import MapObjectNotes
from reamber.sm.mapobj.notes import *
from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class SMMapObjectNotes(MapObjectNotes):

    hits:  SMMapObjectHits  = field(default_factory=lambda: SMMapObjectHits())
    holds: SMMapObjectHolds = field(default_factory=lambda: SMMapObjectHolds())
    rolls: SMMapObjectRolls = field(default_factory=lambda: SMMapObjectRolls())
    mines: SMMapObjectMines = field(default_factory=lambda: SMMapObjectMines())
    lifts: SMMapObjectLifts = field(default_factory=lambda: SMMapObjectLifts())
    fakes: SMMapObjectFakes = field(default_factory=lambda: SMMapObjectFakes())
    keySounds: SMMapObjectKeySounds = field(default_factory=lambda: SMMapObjectKeySounds())

    def columns(self) -> List[int]:
        return self.hits     .columns() + \
               self.holds    .columns() + \
               self.rolls    .columns() + \
               self.mines    .columns() + \
               self.fakes    .columns() + \
               self.lifts    .columns() + \
               self.keySounds.columns()

    def offsets(self) -> List[float]:
        return self.hits     .offsets() + \
               self.holds    .offsets() + \
               self.rolls    .offsets() + \
               self.mines    .offsets() + \
               self.fakes    .offsets() + \
               self.lifts    .offsets() + \
               self.keySounds.offsets()

    def data(self) -> List:
        # noinspection PyTypeChecker
        return self.hits     .data() + \
               self.holds    .data() + \
               self.rolls    .data() + \
               self.mines    .data() + \
               self.fakes    .data() + \
               self.lifts    .data() + \
               self.keySounds.data()

    def __len__(self) -> int:
        return len(self.hits     ) + \
               len(self.holds    ) + \
               len(self.rolls    ) + \
               len(self.mines    ) + \
               len(self.fakes    ) + \
               len(self.lifts    ) + \
               len(self.keySounds)

    def __iter__(self):
        yield self.hits
        yield self.holds
        yield self.rolls
        yield self.mines
        yield self.fakes
        yield self.lifts
        yield self.keySounds

    # I know some may not be "notes" but it covers everything to be safe, as an "expected" result

    def firstOffset(self) -> float:
        return min(self.hits.firstOffset(),
                   self.holds.firstOffset(),
                   self.rolls.firstOffset(),
                   self.mines.firstOffset(),
                   self.lifts.firstOffset(),
                   self.fakes.firstOffset(),
                   self.keySounds.firstOffset())

    def lastOffset(self) -> float:
        return max(self.hits.lastOffset(),
                   self.holds.lastOffset(),
                   self.rolls.lastOffset(),
                   self.mines.lastOffset(),
                   self.lifts.lastOffset(),
                   self.fakes.lastOffset(),
                   self.keySounds.lastOffset())

    def firstLastOffset(self) -> Tuple[float, float]:
        return self.firstOffset(), self.lastOffset()


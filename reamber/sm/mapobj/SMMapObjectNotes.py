from reamber.base.mapobj.MapObjectNotes import MapObjectNotes
from reamber.sm.mapobj.notes import *
from dataclasses import dataclass, field
from typing import List


@dataclass
class SMMapObjectNotes(MapObjectNotes):

    hits:      SMMapObjectHits  = field(default_factory=lambda: SMMapObjectHits())
    holds:     SMMapObjectHolds = field(default_factory=lambda: SMMapObjectHolds())
    rolls:     SMMapObjectRolls = field(default_factory=lambda: SMMapObjectRolls())
    mines:     SMMapObjectMines = field(default_factory=lambda: SMMapObjectMines())
    lifts:     SMMapObjectLifts = field(default_factory=lambda: SMMapObjectLifts())
    fakes:     SMMapObjectFakes = field(default_factory=lambda: SMMapObjectFakes())
    keySounds: SMMapObjectKeySounds = field(default_factory=lambda: SMMapObjectKeySounds())

    def __iter__(self):
        yield self.hits
        yield self.holds
        yield self.rolls
        yield self.mines
        yield self.lifts
        yield self.fakes
        yield self.keySounds

    def data(self) -> List:
        # noinspection PyTypeChecker
        return self.hits     .data() + \
               self.holds    .data() + \
               self.rolls    .data() + \
               self.mines    .data() + \
               self.fakes    .data() + \
               self.lifts    .data() + \
               self.keySounds.data()
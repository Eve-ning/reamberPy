from reamber.base.mapobj.MapObjectNotes import MapObjectNotes
from reamber.sm.mapobj.notes import *
from dataclasses import dataclass, field


@dataclass
class SMMapObjectNotes(MapObjectNotes):
    hits:  SMMapObjectHits  = field(default_factory=lambda: SMMapObjectHits())
    holds: SMMapObjectHolds = field(default_factory=lambda: SMMapObjectHolds())
    rolls: SMMapObjectRolls = field(default_factory=lambda: SMMapObjectRolls())
    mines: SMMapObjectMines = field(default_factory=lambda: SMMapObjectMines())
    lifts: SMMapObjectLifts = field(default_factory=lambda: SMMapObjectLifts())
    fakes: SMMapObjectFakes = field(default_factory=lambda: SMMapObjectFakes())
    keySounds: SMMapObjectKeySounds = field(default_factory=lambda: SMMapObjectKeySounds())

    # I know some may not be "notes" but it covers everything to be safe, as an "expected" result

    def firstOffset(self):
        return min(self.hits.firstOffset(),
                   self.holds.firstOffset(),
                   self.rolls.firstOffset(),
                   self.mines.firstOffset(),
                   self.lifts.firstOffset(),
                   self.fakes.firstOffset(),
                   self.keySounds.firstOffset())

    def lastOffset(self):
        return max(self.hits.lastOffset(),
                   self.holds.lastOffset(),
                   self.rolls.lastOffset(),
                   self.mines.lastOffset(),
                   self.lifts.lastOffset(),
                   self.fakes.lastOffset(),
                   self.keySounds.lastOffset())

    def firstLastOffset(self):
        return self.firstOffset(), self.lastOffset()


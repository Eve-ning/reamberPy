from reamber.base.lists.NotePkg import NotePkg
from reamber.sm.lists.notes import *
from dataclasses import dataclass, field
from typing import List


@dataclass
class SMNotePkg(NotePkg):

    hits:      SMHitList  = field(default_factory=lambda: SMHitList())
    holds:     SMHoldList = field(default_factory=lambda: SMHoldList())
    rolls:     SMRollList = field(default_factory=lambda: SMRollList())
    mines:     SMMineList = field(default_factory=lambda: SMMineList())
    lifts:     SMLiftList = field(default_factory=lambda: SMLiftList())
    fakes:     SMFakeList = field(default_factory=lambda: SMFakeList())
    keySounds: SMKeySoundList = field(default_factory=lambda: SMKeySoundList())

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

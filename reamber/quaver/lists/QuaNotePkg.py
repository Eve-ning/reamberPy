from reamber.base.lists.NotePkg import NotePkg
from reamber.quaver.lists.notes.QuaHitList import QuaHitList
from reamber.quaver.lists.notes.QuaHoldList import QuaHoldList
from dataclasses import dataclass, field
from typing import List


@dataclass
class QuaNotePkg(NotePkg):

    hits: QuaHitList = field(default_factory=lambda: QuaHitList())
    holds: QuaHoldList = field(default_factory=lambda: QuaHoldList())

    def __iter__(self):
        yield self.hits
        yield self.holds

    def data(self) -> List:
        # noinspection PyTypeChecker
        return self.hits.data() + self.holds.data()

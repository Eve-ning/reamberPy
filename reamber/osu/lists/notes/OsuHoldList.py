from reamber.osu.lists.notes.OsuNoteList import OsuNoteList
from reamber.osu.OsuHoldObject import OsuHoldObject
from typing import List


class OsuHoldList(List[OsuHoldObject], OsuNoteList):
    def data(self) -> List[OsuHoldObject]:
        return self

    def lengths(self) -> List[float]:
        return self.attributes('length')

    def tailOffsets(self) -> List[float]:
        return [obj() for obj in self.attributes('tailOffset')]

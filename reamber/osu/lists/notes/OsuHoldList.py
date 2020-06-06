from reamber.osu.lists.notes.OsuNoteList import OsuNoteList
from reamber.osu.OsuHoldObj import OsuHoldObj
from typing import List


class OsuHoldList(List[OsuHoldObj], OsuNoteList):
    def data(self) -> List[OsuHoldObj]:
        return self

    def lengths(self) -> List[float]:
        return self.attributes('length')

    def tailOffsets(self) -> List[float]:
        return [obj() for obj in self.attributes('tailOffset')]

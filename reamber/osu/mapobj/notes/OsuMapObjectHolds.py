from reamber.osu.mapobj.notes.OsuMapObjectNoteBase import OsuMapObjectNoteBase
from reamber.osu.OsuHoldObject import OsuHoldObject
from typing import List


class OsuMapObjectHolds(List[OsuHoldObject], OsuMapObjectNoteBase):
    def data(self) -> List[OsuHoldObject]:
        return self

    def lengths(self) -> List[float]:
        return self.attributes('length')

    def tailOffsets(self) -> List[float]:
        return [obj() for obj in self.attributes('tailOffset')]

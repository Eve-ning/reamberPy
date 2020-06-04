from reamber.osu.mapobj.notes.OsuMapObjectNoteBase import OsuMapObjectNoteBase
from reamber.osu.OsuHitObject import OsuHitObject
from typing import List


class OsuMapObjectHits(List[OsuHitObject], OsuMapObjectNoteBase):
    def data(self) -> List[OsuHitObject]:
        return self

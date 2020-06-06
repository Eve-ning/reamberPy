from reamber.osu.lists.notes.OsuNoteList import OsuNoteList
from reamber.osu.OsuHitObject import OsuHitObject
from typing import List


class OsuHitList(List[OsuHitObject], OsuNoteList):
    def data(self) -> List[OsuHitObject]:
        return self

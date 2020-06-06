from reamber.osu.lists.notes.OsuNoteList import OsuNoteList
from reamber.osu.OsuHitObj import OsuHitObj
from typing import List


class OsuHitList(List[OsuHitObj], OsuNoteList):
    def data(self) -> List[OsuHitObj]:
        return self

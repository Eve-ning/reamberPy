from reamber.osu.lists.notes.OsuNoteList import OsuNoteList
from reamber.osu.OsuHitObj import OsuHitObj
from typing import List


class OsuHitList(List[OsuHitObj], OsuNoteList):

    def _upcast(self, objList: List = None):
        return OsuHitList(objList)

    def data(self) -> List[OsuHitObj]:
        return self

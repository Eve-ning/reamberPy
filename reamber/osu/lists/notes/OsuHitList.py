from __future__ import annotations
from reamber.osu.lists.notes.OsuNoteList import OsuNoteList
from reamber.osu.OsuHitObj import OsuHitObj
from typing import List


class OsuHitList(List[OsuHitObj], OsuNoteList):

    def _upcast(self, objList: List = None) -> OsuHitList:
        """ This is to facilitate inherited functions to work

        :param objList: The List to cast
        :rtype: OsuHitList
        """
        return OsuHitList(objList)

    def data(self) -> List[OsuHitObj]:
        return self

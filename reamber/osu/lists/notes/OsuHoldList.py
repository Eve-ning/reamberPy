from __future__ import annotations
from reamber.osu.lists.notes.OsuNoteList import OsuNoteList
from reamber.osu.OsuHold import OsuHold
from reamber.base.lists.notes.HoldList import HoldList
from typing import List


class OsuHoldList(List[OsuHold], OsuNoteList, HoldList):

    def _upcast(self, objList: List = None) -> OsuHoldList:
        """ This is to facilitate inherited functions to work

        :param objList: The List to cast
        :rtype: OsuHoldList
        """
        return OsuHoldList(objList)

    def data(self) -> List[OsuHold]:
        return self

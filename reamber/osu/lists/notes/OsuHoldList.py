from __future__ import annotations
from reamber.osu.lists.notes.OsuNoteList import OsuNoteList
from reamber.osu.OsuHoldObj import OsuHoldObj
from reamber.base.lists.notes.HoldList import HoldList
from typing import List


class OsuHoldList(List[OsuHoldObj], OsuNoteList, HoldList):

    def _upcast(self, objList: List = None) -> OsuHoldList:
        """ This is to facilitate inherited functions to work

        :param objList: The List to cast
        :rtype: OsuHoldList
        """
        return OsuHoldList(objList)

    def data(self) -> List[OsuHoldObj]:
        return self

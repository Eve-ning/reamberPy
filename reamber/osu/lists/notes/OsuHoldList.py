from __future__ import annotations

from typing import List

from reamber.base.lists.notes.HoldList import HoldList
from reamber.osu.OsuHold import OsuHold
from reamber.osu.lists.notes.OsuNoteList import OsuNoteList


class OsuHoldList(List[OsuHold], HoldList, OsuNoteList):

    def _upcast(self, obj_list: List = None) -> OsuHoldList:
        """ This is to facilitate inherited functions to work

        :param obj_list: The List to cast
        :rtype: OsuHoldList
        """
        return OsuHoldList(obj_list)

    def mult_offset(self, by: float, inplace:bool = False):
        HoldList.mult_offset(self, by=by, inplace=inplace)

    def data(self) -> List[OsuHold]:
        return self


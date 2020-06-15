from __future__ import annotations

from reamber.osu.lists.notes.OsuNoteList import OsuNoteList
from reamber.osu.OsuHoldObj import OsuHoldObj
from typing import List


class OsuHoldList(List[OsuHoldObj], OsuNoteList):

    def _upcast(self, objList: List = None) -> OsuHoldList:
        """ This is to facilitate inherited functions to work

        :param objList: The List to cast
        :rtype: OsuHoldList
        """
        return OsuHoldList(objList)

    def data(self) -> List[OsuHoldObj]:
        return self

    def lengths(self) -> List[float]:
        return self.attribute('length')

    def offsets(self, flatten=True):
        if flatten: return [i for j in [(obj.offset, obj.tailOffset()) for obj in self.data()] for i in j]
        return [(obj.offset, obj.tailOffset()) for obj in self.data()]

    def tailOffsets(self) -> List[float]:
        return [obj() for obj in self.attribute('tailOffset')]

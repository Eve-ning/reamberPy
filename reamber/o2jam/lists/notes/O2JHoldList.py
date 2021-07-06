from __future__ import annotations

from typing import List

from reamber.base.lists.notes.HoldList import HoldList
from reamber.o2jam.O2JHold import O2JHold
from reamber.o2jam.lists.notes.O2JNoteList import O2JNoteList


class O2JHoldList(List[O2JHold], HoldList, O2JNoteList):

    def _upcast(self, objList: List = None) -> O2JNoteList:
        """ This is to facilitate inherited functions to work

        :param objList: The List to cast
        :rtype: O2JNoteList
        """
        return O2JHoldList(objList)

    def mult_offset(self, by: float, inplace:bool = False):
        HoldList.mult_offset(self, by=by, inplace=inplace)

    def data(self) -> List[O2JHold]:
        return self

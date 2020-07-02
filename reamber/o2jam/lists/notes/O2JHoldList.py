from __future__ import annotations
from reamber.o2jam.lists.notes.O2JNoteList import O2JNoteList
from reamber.o2jam.O2JHold import O2JHold
from reamber.base.lists.notes.HoldList import HoldList
from typing import List


class O2JHoldList(List[O2JHold], HoldList, O2JNoteList):

    def _upcast(self, objList: List = None) -> O2JNoteList:
        """ This is to facilitate inherited functions to work

        :param objList: The List to cast
        :rtype: O2JNoteList
        """
        return O2JHoldList(objList)

    def multOffset(self, by: float, inplace:bool = False):
        HoldList.multOffset(self, by=by, inplace=inplace)

    def data(self) -> List[O2JHold]:
        return self

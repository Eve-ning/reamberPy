from __future__ import annotations
from reamber.o2jam.lists.notes.O2JNoteList import O2JNoteList
from reamber.o2jam.O2JHold import O2JHold
from reamber.base.lists.notes.HoldList import HoldList
from typing import List


class O2JHoldList(List[O2JHold], O2JNoteList, HoldList):

    def _upcast(self, objList: List = None) -> O2JNoteList:
        """ This is to facilitate inherited functions to work

        :param objList: The List to cast
        :rtype: O2JNoteList
        """
        return O2JHoldList(objList)

    def data(self) -> List[O2JHold]:
        return self

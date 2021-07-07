from __future__ import annotations

from typing import List

from reamber.o2jam.O2JHit import O2JHit
from reamber.o2jam.lists.notes.O2JNoteList import O2JNoteList


class O2JHitList(List[O2JHit], O2JNoteList):

    def _upcast(self, obj_list: List = None) -> O2JHitList:
        """ This is to facilitate inherited functions to work

        :param obj_list: The List to cast
        :rtype: O2JHitList
        """
        return O2JHitList(obj_list)

    def data(self) -> List[O2JHit]:
        return self

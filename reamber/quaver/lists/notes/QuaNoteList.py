from __future__ import annotations

from abc import ABC
from typing import List, Type

from reamber.base.lists.notes.NoteList import NoteList
from reamber.quaver.QuaNoteMeta import QuaNoteMeta


class QuaNoteList(NoteList, ABC):

    def _upcast(self, objList: List = None) -> QuaNoteList:
        """ This is to facilitate inherited functions to work

        :param objList: The List to cast
        :rtype: QuaNoteList
        """
        return QuaNoteList(objList)

    def data(self) -> List[Type[QuaNoteMeta]]: pass

    def keySoundsList(self):
        return self.attribute('keySounds')

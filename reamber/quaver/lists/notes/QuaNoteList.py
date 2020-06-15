from __future__ import annotations
from reamber.base.lists.notes.NoteList import NoteList
from typing import List, Type
from abc import ABC

from reamber.quaver.QuaNoteObjMeta import QuaNoteObjMeta


class QuaNoteList(NoteList, ABC):

    def _upcast(self, objList: List = None) -> QuaNoteList:
        """ This is to facilitate inherited functions to work

        :param objList: The List to cast
        :rtype: QuaNoteList
        """
        return QuaNoteList(objList)

    def data(self) -> List[Type[QuaNoteObjMeta]]: pass

    def keySoundsList(self):
        return self.attribute('keySounds')

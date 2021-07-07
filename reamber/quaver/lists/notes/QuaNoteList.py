from __future__ import annotations

from abc import ABC
from typing import List, Type

from reamber.base.lists.notes.NoteList import NoteList
from reamber.quaver.QuaNoteMeta import QuaNoteMeta


class QuaNoteList(NoteList, ABC):

    def _upcast(self, obj_list: List = None) -> QuaNoteList:
        """ This is to facilitate inherited functions to work

        :param obj_list: The List to cast
        :rtype: QuaNoteList
        """
        return QuaNoteList(obj_list)

    def data(self) -> List[Type[QuaNoteMeta]]: pass

    def key_sounds_list(self):
        return self.attribute('keySounds')

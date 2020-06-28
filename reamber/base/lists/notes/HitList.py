from __future__ import annotations
from typing import List
from reamber.base.Hit import Hit
from reamber.base.lists.notes.NoteList import NoteList
from abc import ABC


class HitList(List[Hit], NoteList, ABC):
    """ Deprecated, don't think this is useful """

    def data(self) -> List[Hit]:
        return self


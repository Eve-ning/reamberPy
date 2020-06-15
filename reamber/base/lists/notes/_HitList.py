from __future__ import annotations
from typing import List
from reamber.base.HitObj import HitObj
from reamber.base.lists.notes.NoteList import NoteList
from abc import ABC


class HitList(List[HitObj], NoteList, ABC):
    """ Deprecated, don't think this is useful """

    def data(self) -> List[HitObj]:
        return self


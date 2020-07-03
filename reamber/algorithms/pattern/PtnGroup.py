from __future__ import annotations
from reamber.algorithms.pattern.PtnNote import PtnNote
from reamber.base.Note import Note
from reamber.base.lists.notes.NoteList import NoteList
from typing import List


class PtnGroup(List[PtnNote], NoteList):
    """ Just a subclass to separate the interfaces. """

    def __init__(self, list_, confidence:List or float = 1.0):
        list.__init__(self, [])

        if isinstance(confidence, (float, int)): confidence = [confidence for i in range(list_)]
        elif isinstance(confidence, List): assert len(confidence) == len(list_), "Both lengths must be the same."

        for i in range(len(list_)):
            if isinstance(list_[i], Note):
                list_[i] = PtnNote(list_[i].offset,
                                   list_[i].column,
                                   confidence=confidence[i])

        list.__init__(self, list_)

    def data(self) -> List[PtnNote]:
        return self

    def __len__(self):
        return super().__len__()

    def _upcast(self, objList: List = None):
        return PtnGroup(objList)


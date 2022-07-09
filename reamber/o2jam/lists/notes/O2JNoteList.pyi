from abc import ABC
from typing import TypeVar

from reamber.base.lists.notes.NoteList import NoteList

Item = TypeVar('Item')


class O2JNoteList(NoteList[Item], ABC):
    ...

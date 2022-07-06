from abc import ABC
from typing import TypeVar

from reamber.base.Property import list_props
from reamber.base.lists.notes.NoteList import NoteList
from reamber.o2jam import O2JHit

Item = TypeVar('Item')


@list_props(O2JHit)
class O2JNoteList(NoteList[Item], ABC):
    ...

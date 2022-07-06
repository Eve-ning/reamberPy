from abc import ABC
from typing import TypeVar

from reamber.base.Property import list_props
from reamber.base.lists.notes.NoteList import NoteList
from reamber.sm.SMHit import SMHit

Item = TypeVar('Item')


@list_props(SMHit)
class SMNoteList(NoteList[Item], ABC):
    ...

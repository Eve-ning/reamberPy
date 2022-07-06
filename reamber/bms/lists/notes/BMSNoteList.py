from abc import ABC
from typing import TypeVar

from reamber.base.Property import list_props
from reamber.base.lists.notes.NoteList import NoteList
from reamber.bms.BMSHit import BMSHit

Item = TypeVar('Item')


@list_props(BMSHit)
class BMSNoteList(NoteList[Item], ABC):
    ...

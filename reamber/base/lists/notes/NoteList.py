from __future__ import annotations

from typing import TypeVar

from reamber.base.Note import Note
from reamber.base.Property import list_props
from reamber.base.lists.TimedList import TimedList

Item = TypeVar('Item')


@list_props(Note)
class NoteList(TimedList[Item]):
    """Extends from the TimedList to give more base functions to Notes"""
    ...

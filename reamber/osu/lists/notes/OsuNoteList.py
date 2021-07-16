from __future__ import annotations

from abc import ABC
from typing import List, Type, overload, Any, Union, Generator, TypeVar


from reamber.base.Property import list_props
from reamber.base.lists.notes.NoteList import NoteList
from reamber.osu import OsuHit

Item = TypeVar('Item')

@list_props(OsuHit)
class OsuNoteList(NoteList[Item], ABC):
    ...

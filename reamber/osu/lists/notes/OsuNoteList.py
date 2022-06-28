from __future__ import annotations

from abc import ABC
from typing import TypeVar


from reamber.base.Property import list_props
from reamber.base.lists.notes.NoteList import NoteList
from reamber.osu.OsuHit import OsuHit

Item = TypeVar('Item')

@list_props(OsuHit)
class OsuNoteList(NoteList[Item], ABC):
    ...

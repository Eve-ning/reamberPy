from __future__ import annotations

from reamber.base.Property import list_props
from reamber.base.lists.notes.HitList import HitList
from reamber.sm.SMLift import SMLift
from reamber.sm.lists.notes.SMNoteList import SMNoteList


@list_props(SMLift)
class SMLiftList(HitList[SMLift], SMNoteList[SMLift]):
    ...

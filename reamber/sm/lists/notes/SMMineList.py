from __future__ import annotations

from reamber.base.Property import list_props
from reamber.base.lists.notes.HitList import HitList
from reamber.sm.SMMine import SMMine
from reamber.sm.lists.notes.SMNoteList import SMNoteList


@list_props(SMMine)
class SMMineList(HitList[SMMine], SMNoteList[SMMine]):
    ...

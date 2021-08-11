from __future__ import annotations

from reamber.base.Property import list_props
from reamber.base.lists.notes.HitList import HitList
from reamber.sm.SMHit import SMHit
from reamber.sm.lists.notes.SMNoteList import SMNoteList


@list_props(SMHit)
class SMHitList(HitList[SMHit], SMNoteList[SMHit]):
    ...

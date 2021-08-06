from __future__ import annotations

from reamber.base.lists.notes.HitList import HitList
from reamber.sm.SMHit import SMHit
from reamber.sm.lists.notes.SMNoteList import SMNoteList


class SMHitList(HitList[SMHit], SMNoteList[SMHit]):
    ...

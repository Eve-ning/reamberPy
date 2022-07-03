from __future__ import annotations

from reamber.base.lists.notes.HitList import HitList
from reamber.bms.BMSHit import BMSHit
from reamber.bms.lists.notes.BMSNoteList import BMSNoteList


class BMSHitList(HitList[BMSHit], BMSNoteList[BMSHit]):
    ...

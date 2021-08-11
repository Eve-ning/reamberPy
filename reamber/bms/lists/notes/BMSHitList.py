from __future__ import annotations

from reamber.base.Property import list_props
from reamber.base.lists.notes.HitList import HitList
from reamber.bms.BMSHit import BMSHit
from reamber.bms.lists.notes.BMSNoteList import BMSNoteList


@list_props(BMSHit)
class BMSHitList(HitList[BMSHit], BMSNoteList[BMSHit]):
    ...

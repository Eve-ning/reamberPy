from __future__ import annotations

from reamber.base.Property import list_props
from reamber.base.lists.notes import HitList
from reamber.o2jam.O2JHit import O2JHit
from reamber.o2jam.lists.notes.O2JNoteList import O2JNoteList


@list_props(O2JHit)
class O2JHitList(HitList[O2JHit], O2JNoteList[O2JHit]):
    ...

from __future__ import annotations

from reamber.base.Property import list_props
from reamber.base.lists.notes.HitList import HitList
from reamber.sm.SMFake import SMFake
from reamber.sm.lists.notes.SMNoteList import SMNoteList


@list_props(SMFake)
class SMFakeList(HitList[SMFake], SMNoteList[SMFake]):
    ...

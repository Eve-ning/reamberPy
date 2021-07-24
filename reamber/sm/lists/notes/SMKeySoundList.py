from __future__ import annotations

from reamber.base.Property import list_props
from reamber.base.lists.notes.HitList import HitList
from reamber.sm import SMKeySound
from reamber.sm.lists.notes import SMNoteList


@list_props(SMKeySound)
class SMKeySoundList(HitList[SMKeySound], SMNoteList[SMKeySound]):
    ...

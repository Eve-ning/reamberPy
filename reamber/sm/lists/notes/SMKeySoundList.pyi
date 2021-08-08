from __future__ import annotations

from reamber.base.lists.notes.HitList import HitList
from reamber.sm.SMKeySound import SMKeySound
from reamber.sm.lists.notes.SMNoteList import SMNoteList


class SMKeySoundList(HitList[SMKeySound], SMNoteList[SMKeySound]):
    ...

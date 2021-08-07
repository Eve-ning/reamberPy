from __future__ import annotations

from reamber.base.lists.notes.HoldList import HoldList
from reamber.sm.SMRoll import SMRoll
from reamber.sm.lists.notes.SMNoteList import SMNoteList


class SMRollList(HoldList[SMRoll], SMNoteList[SMRoll]):
    ...

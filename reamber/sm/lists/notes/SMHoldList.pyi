from __future__ import annotations

from reamber.base.lists.notes.HoldList import HoldList
from reamber.sm.SMHold import SMHold
from reamber.sm.lists.notes.SMNoteList import SMNoteList


class SMHoldList(HoldList[SMHold], SMNoteList[SMHold]):
    ...

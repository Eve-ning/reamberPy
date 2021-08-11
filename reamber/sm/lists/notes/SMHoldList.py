from __future__ import annotations

from reamber.base.Property import list_props
from reamber.base.lists.notes.HoldList import HoldList
from reamber.sm.SMHold import SMHold
from reamber.sm.lists.notes.SMNoteList import SMNoteList


@list_props(SMHold)
class SMHoldList(HoldList[SMHold], SMNoteList[SMHold]):
    ...

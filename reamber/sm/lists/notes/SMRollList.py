from __future__ import annotations

from reamber.base.Property import list_props
from reamber.base.lists.notes.HoldList import HoldList
from reamber.sm.SMRoll import SMRoll
from reamber.sm.lists.notes.SMNoteList import SMNoteList


@list_props(SMRoll)
class SMRollList(HoldList[SMRoll], SMNoteList[SMRoll]):
    ...

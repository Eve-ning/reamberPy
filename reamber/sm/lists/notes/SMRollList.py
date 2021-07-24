from __future__ import annotations

from reamber.base.Property import list_props
from reamber.base.lists.notes.HoldList import HoldList
from reamber.osu.OsuHold import OsuHold
from reamber.sm import SMRoll
from reamber.sm.lists.notes import SMNoteList


@list_props(OsuHold)
class SMRollList(HoldList[SMRoll], SMNoteList[SMRoll]):
    ...

from __future__ import annotations

from reamber.base.Property import list_props
from reamber.base.lists.notes.HoldList import HoldList
from reamber.bms.BMSHold import BMSHold
from reamber.bms.lists.notes.BMSNoteList import BMSNoteList


@list_props(BMSHold)
class BMSHoldList(HoldList[BMSHold], BMSNoteList[BMSHold]):
    ...

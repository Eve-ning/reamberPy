from __future__ import annotations

from reamber.base.lists.notes.HoldList import HoldList
from reamber.bms.BMSHold import BMSHold
from reamber.bms.lists.notes.BMSNoteList import BMSNoteList


class BMSHoldList(HoldList[BMSHold], BMSNoteList[BMSHold]):
    ...

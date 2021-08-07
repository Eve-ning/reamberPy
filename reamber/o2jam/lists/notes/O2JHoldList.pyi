from __future__ import annotations

from reamber.base.lists.notes.HoldList import HoldList
from reamber.o2jam.O2JHold import O2JHold
from reamber.o2jam.lists.notes.O2JNoteList import O2JNoteList


class O2JHoldList(HoldList[O2JHold], O2JNoteList):
    ...

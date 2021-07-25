from __future__ import annotations

from reamber.base.Property import list_props
from reamber.base.lists.BpmList import BpmList
from reamber.base.lists.TimedList import TimedList
from reamber.sm import SMBpm, SMStop


@list_props(SMStop)
class SMStopList(TimedList[SMStop]):
    ...

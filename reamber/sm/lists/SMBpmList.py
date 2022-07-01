from __future__ import annotations

from reamber.base.Property import list_props
from reamber.base.lists.BpmList import BpmList
from reamber.sm import SMBpm


@list_props(SMBpm)
class SMBpmList(BpmList[SMBpm]):
    ...

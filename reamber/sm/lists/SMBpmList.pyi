from __future__ import annotations

from reamber.base.lists.BpmList import BpmList
from reamber.sm import SMBpm


class SMBpmList(BpmList[SMBpm]):
    def reseat(self, item_class=SMBpm) -> SMBpmList: ...


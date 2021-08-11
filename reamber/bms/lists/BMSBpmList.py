from __future__ import annotations

from reamber.base.Property import list_props
from reamber.base.lists.BpmList import BpmList
from reamber.bms.BMSBpm import BMSBpm


@list_props(BMSBpm)
class BMSBpmList(BpmList[BMSBpm]):
    ...

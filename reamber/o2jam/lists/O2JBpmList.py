from __future__ import annotations

from reamber.base.Property import list_props
from reamber.base.lists.BpmList import BpmList
from reamber.o2jam.O2JBpm import O2JBpm


@list_props(O2JBpm)
class O2JBpmList(BpmList[O2JBpm]):
    ...

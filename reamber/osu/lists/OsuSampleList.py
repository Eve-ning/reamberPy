from __future__ import annotations

from reamber.base.Property import list_props
from reamber.base.lists.TimedList import TimedList
from reamber.osu.OsuSample import OsuSample

@list_props(OsuSample)
class OsuSampleList(TimedList[OsuSample]):
    pass


from __future__ import annotations

from typing import List

from reamber.base.Property import list_props
from reamber.base.lists.TimedList import TimedList
from reamber.osu.OsuSample import OsuSample

@list_props(OsuSample)
class OsuSampleList(List[OsuSample], TimedList):

    def data(self) -> List[OsuSample]:
        return self


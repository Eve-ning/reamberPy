from __future__ import annotations

from typing import List

import pandas as pd

from reamber.base.Property import list_props
from reamber.base.lists.BpmList import BpmList
from reamber.osu.OsuBpm import OsuBpm


@list_props(OsuBpm)
class OsuBpmList(BpmList[OsuBpm]):

    @staticmethod
    def read(strings: List[str]) -> OsuBpmList:
        return OsuBpmList(pd.DataFrame(
            [OsuBpm.read_string(s, as_dict=True) for s in strings]
        ) if strings else [])

    def write(self) -> List[str]:
        return [h.write_string() for h in self]

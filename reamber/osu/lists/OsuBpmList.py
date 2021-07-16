from __future__ import annotations

from typing import List, overload, Any, Generator

from reamber.base.Property import list_props
from reamber.base.lists.BpmList import BpmList
from reamber.osu.OsuBpm import OsuBpm


@list_props(OsuBpm)
class OsuBpmList(BpmList[OsuBpm]):

    @staticmethod
    def read(strings: List[str]) -> OsuBpmList:
        """ A shortcut to reading OsuHit in a loop to create a OsuHitList

        :param strings: A List of strings to loop through OsuHit.read
        """
        return OsuBpmList([OsuBpm.read_string(s) for s in strings])

    def write(self) -> List[str]:
        return [h.write_string() for h in self]



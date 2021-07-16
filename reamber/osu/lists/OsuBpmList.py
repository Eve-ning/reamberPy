from __future__ import annotations

from typing import List, overload, Any, Generator

from reamber.base.lists.BpmList import BpmList
from reamber.osu.OsuBpm import OsuBpm


class OsuBpmList(BpmList[OsuBpm]):

    @property
    def _init_empty(self) -> dict:
        """ Initializes the DataFrame if no objects are passed to init. """
        return dict(**super(OsuBpmList, self)._init_empty)

    @staticmethod
    def read(strings: List[str]) -> OsuBpmList:
        """ A shortcut to reading OsuHit in a loop to create a OsuHitList

        :param strings: A List of strings to loop through OsuHit.read
        """
        return OsuBpmList([OsuBpm.read_string(s) for s in strings])

    def write(self) -> List[str]:
        return [h.write_string() for h in self]

from __future__ import annotations

from typing import List, Generator

from reamber.base.lists.TimedList import TimedList
from reamber.osu.OsuSv import OsuSv


class OsuSvList(TimedList[OsuSv]):

    @staticmethod
    def _init_empty() -> dict:
        """ Initializes the DataFrame if no objects are passed to init. """
        return dict(**TimedList._init_empty())

    @staticmethod
    def read(strings: List[str]) -> OsuSvList:
        """ A shortcut to reading OsuHit in a loop to create a OsuHitList

        :param strings: A List of strings to loop through OsuHit.read
        """
        return OsuSvList([OsuSv.read_string(s) for s in strings])

    def write(self) -> List[str]:
        return [h.write_string() for h in self]

    def multipliers(self) -> List[float]:
        """ Gets all Scroll Velocity values """
        return self.attribute('multiplier')


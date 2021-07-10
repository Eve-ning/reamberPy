from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from dataclasses import field
from typing import List

from reamber.base.Map import Map


@dataclass
class MapSet:

    maps: List[Map] = field(default_factory=lambda: [])

    def deepcopy(self):
        """ Returns a deep copy of itself """
        return deepcopy(self)

    def describe(self, rounding: int = 2, unicode: bool = False) -> None:
        """ Describes the map's attributes as a short summary

        :param rounding: The decimal rounding
        :param unicode: Whether to attempt to get the non-unicode or unicode. \
            Doesn't attempt to translate.
        """

        for m in self.maps:
            m.describe(rounding=rounding, unicode=unicode, s=self)
            print("="*20)

    def rate(self, by: float) -> MapSet:
        """ Changes the rate of the map. Note that you need to do rate on the mapset to affect BPM.

        :param by: The value to rate it by. 1.1x speeds up the song by 10%. Hence 10/11 of the length.
        """

        return MapSet([m.rate(by=by) for m in self.maps])

from __future__ import annotations

from copy import deepcopy
from typing import List, Dict, Iterator

from reamber.base.Map import Map
from reamber.base.lists import TimedList


class MapSet:

    maps: List[Map]

    def __init__(self, maps: List[Map]):
        self._maps = maps

    def __iter__(self) -> Iterator[Map]:
        for m in self.maps:
            yield m

    @property
    def maps(self):
        return self._maps

    @maps.setter
    def maps(self, val):
        self._maps = val

    @property
    def offsets(self) -> List[Dict[str, TimedList]]:
        return [m.offsets for m in self.maps]

    @offsets.setter
    def offsets(self, val: List[Dict[str, TimedList]]):
        for m, v in zip(self.maps, val):
            m.offsets = v

    def deepcopy(self):
        """ Returns a deep copy of itself """
        return deepcopy(self)

    def describe(self, rounding: int = 2, unicode: bool = False) -> List[str]:
        """ Describes the map's attributes as a short summary

        :param rounding: The decimal rounding
        :param unicode: Whether to attempt to get the non-unicode or unicode. \
            Doesn't attempt to translate.
        """

        return [m.describe(rounding=rounding, unicode=unicode) for m in self.maps]

    def rate(self, by: float) -> MapSet:
        """ Changes the rate of the map. Note that you need to do rate on the mapset to affect BPM.

        :param by: The value to rate it by. 1.1x speeds up the song by 10%. Hence 10/11 of the length.
        """

        return MapSet([m.rate(by=by) for m in self.maps])

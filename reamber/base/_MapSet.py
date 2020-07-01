""" Do we still need this ?
Leaving it here just in case

TODO: Decide on if this should be axed"""

from typing import List
from dataclasses import dataclass
from dataclasses import field

from reamber.base.Map import Map


@dataclass
class MapSet:

    maps: List[Map] = field(default_factory=lambda: [])

    def describe(self, rounding: int = 2, unicode: bool = False) -> None:
        """ Describes the map's attributes as a short summary

        :param rounding: The decimal rounding
        :param unicode: Whether to attempt to get the non-unicode or unicode. \
            Doesn't attempt to translate.
        """

        for m in self.maps:
            m.describe(rounding=rounding, unicode=unicode, s=self)
            print("="*20)

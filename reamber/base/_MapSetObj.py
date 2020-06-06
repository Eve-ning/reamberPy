""" Do we still need this ?
Leaving it here just in case

TODO: Decide on if this should be axed"""

from typing import List
from dataclasses import dataclass
from dataclasses import field

from reamber.base.MapObj import MapObj


@dataclass
class MapSetObj:
    maps: List[MapObj] = field(default_factory=lambda: [])

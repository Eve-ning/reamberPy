""" Do we still need this ?
Leaving it here just in case

TODO: Decide on if this should be axed"""

from typing import List
from dataclasses import dataclass
from dataclasses import field

from reamber.base.MapObject import MapObject


@dataclass
class MapSetObject:
    maps: List[MapObject] = field(default_factory=lambda: [])

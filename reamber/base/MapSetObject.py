from typing import List
from dataclasses import dataclass
from dataclasses import field

from reamber.base.MapObject import MapObject


@dataclass
class MapSetObject:
    maps: List[MapObject] = field(default_factory=lambda: [])

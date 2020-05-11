from typing import List
from dataclasses import dataclass
from dataclasses import field

from src.base.MapObject import MapObject


@dataclass
class MapSetObject:
    maps: List[MapObject] = field(default_factory=lambda: [])

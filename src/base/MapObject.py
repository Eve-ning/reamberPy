from typing import List
from typing import Type
from dataclasses import dataclass
from dataclasses import field

from src.base.HitObject import HitObject
from src.base.TimingPoint import TimingPoint


@dataclass
class MapObject:
    hitObjects: List[Type[HitObject]] = field(default_factory=lambda: [])
    timingPoints: List[Type[TimingPoint]] = field(default_factory=lambda: [])

from src.base.HitObject import HitObject as HitObject
from dataclasses import dataclass


@dataclass
class HoldObject(HitObject):
    length: float = 0.0

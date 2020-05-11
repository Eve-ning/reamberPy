from reamber.base.HitObject import HitObject
from dataclasses import dataclass


@dataclass
class SMHitObject(HitObject):
    STRING: str = "1"
    pass

from reamber.base.HitObject import HitObject
from dataclasses import dataclass


@dataclass
class SMMineObject(HitObject):
    STRING: str = "M"
    pass

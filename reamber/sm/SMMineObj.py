from reamber.base.HitObj import HitObj
from dataclasses import dataclass


@dataclass
class SMMineObj(HitObj):
    STRING: str = "M"
    pass

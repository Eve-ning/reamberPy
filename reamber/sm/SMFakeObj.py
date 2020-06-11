from reamber.base.HitObj import HitObj
from dataclasses import dataclass


@dataclass
class SMFakeObj(HitObj):
    STRING: str = "F"
    pass

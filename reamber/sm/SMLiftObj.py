from reamber.base.HitObj import HitObj
from dataclasses import dataclass


@dataclass
class SMLiftObj(HitObj):
    STRING: str = "L"
    pass

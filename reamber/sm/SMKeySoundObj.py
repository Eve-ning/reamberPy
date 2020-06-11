from reamber.base.HitObj import HitObj
from dataclasses import dataclass


@dataclass
class SMKeySoundObj(HitObj):
    STRING: str = "K"
    pass

from src.base.HitObject import HitObject
from dataclasses import dataclass


@dataclass
class SMKeySoundObject(HitObject):
    STRING: str = "K"
    pass

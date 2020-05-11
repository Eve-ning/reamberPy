from src.base.HitObject import HitObject
from dataclasses import dataclass


@dataclass
class SMFakeObject(HitObject):
    STRING: str = "F"
    pass

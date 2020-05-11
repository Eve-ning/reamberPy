from src.base.HitObject import HitObject
from dataclasses import dataclass


@dataclass
class SMLiftObject(HitObject):
    STRING: str = "L"
    pass

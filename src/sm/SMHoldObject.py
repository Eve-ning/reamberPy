from src.base.HoldObject import HoldObject
from dataclasses import dataclass


@dataclass
class SMHoldObject(HoldObject):
    STRING_HEAD: str = "2"
    STRING_TAIL: str = "3"
    pass

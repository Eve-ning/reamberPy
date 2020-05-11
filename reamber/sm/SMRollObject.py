from reamber.base.HoldObject import HoldObject
from dataclasses import dataclass


@dataclass
class SMRollObject(HoldObject):
    STRING_HEAD: str = "4"
    STRING_TAIL: str = "3"
    pass

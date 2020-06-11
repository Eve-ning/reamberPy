from reamber.base.HoldObj import HoldObj
from dataclasses import dataclass


@dataclass
class SMHoldObj(HoldObj):
    STRING_HEAD: str = "2"
    STRING_TAIL: str = "3"
    pass

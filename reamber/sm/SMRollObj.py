from reamber.base.HoldObj import HoldObj
from dataclasses import dataclass


@dataclass
class SMRollObj(HoldObj):
    STRING_HEAD: str = "4"
    STRING_TAIL: str = "3"
    pass

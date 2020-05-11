from reamber.base.TimedObject import TimedObject
from dataclasses import dataclass


@dataclass
class SMStop(TimedObject):
    length: float = 0

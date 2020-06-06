from reamber.base.TimedObject import TimedObject
from dataclasses import dataclass


@dataclass
class SMStopObject(TimedObject):
    length: float = 0

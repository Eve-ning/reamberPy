from reamber.base.TimedObj import TimedObj
from dataclasses import dataclass


@dataclass
class SMStopObj(TimedObj):
    length: float = 0

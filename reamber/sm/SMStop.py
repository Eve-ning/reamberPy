from reamber.base.Timed import Timed
from dataclasses import dataclass


@dataclass
class SMStop(Timed):
    length: float = 0

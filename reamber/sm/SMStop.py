from dataclasses import dataclass

from reamber.base.Timed import Timed


@dataclass
class SMStop(Timed):
    length: float = 0

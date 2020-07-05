from __future__ import annotations
from reamber.base.Timed import Timed
from dataclasses import dataclass

MIN_SV = 0.01
MAX_SV = 10.0

@dataclass
class DmSv(Timed):
    multiplier: float = 1.0
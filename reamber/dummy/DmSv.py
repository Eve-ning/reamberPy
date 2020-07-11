from __future__ import annotations

from dataclasses import dataclass

from reamber.base.Timed import Timed

MIN_SV = 0.01
MAX_SV = 10.0

@dataclass
class DmSv(Timed):
    multiplier: float = 1.0
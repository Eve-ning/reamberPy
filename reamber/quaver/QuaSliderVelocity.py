from reamber.base.TimedObject import TimedObject
from dataclasses import dataclass
from typing import Dict


@dataclass
class QuaSliderVelocity(TimedObject):
    multiplier: float = 1.0

    def asDict(self) -> Dict:
        return {"StartTime": self.offset,
                "Multiplier": self.multiplier}

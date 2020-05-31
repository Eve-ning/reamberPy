from reamber.base.BpmPoint import BpmPoint
from dataclasses import dataclass
from typing import Dict


@dataclass
class QuaBpmPoint(BpmPoint):
    def asDict(self) -> Dict:
        return {
            "StartTime": self.offset,
            "Bpm": self.bpm
        }

from reamber.base.BpmObject import BpmObject
from dataclasses import dataclass
from typing import Dict


@dataclass
class QuaBpmObject(BpmObject):
    def asDict(self) -> Dict:
        return {
            "StartTime": self.offset,
            "Bpm": self.bpm
        }

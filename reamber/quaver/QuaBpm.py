from reamber.base.Bpm import Bpm
from dataclasses import dataclass
from typing import Dict


@dataclass
class QuaBpm(Bpm):
    def asDict(self) -> Dict:
        """ Used to facilitate exporting as Qua from YAML """
        return {
            "StartTime": self.offset,
            "Bpm": self.bpm
        }

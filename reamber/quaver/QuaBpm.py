from dataclasses import dataclass
from typing import Dict

from reamber.base.Bpm import Bpm


@dataclass
class QuaBpm(Bpm):
    def asDict(self) -> Dict:
        """ Used to facilitate exporting as Qua from YAML """
        return {
            "StartTime": self.offset,
            "Bpm": self.bpm
        }

from dataclasses import dataclass
from typing import Dict

from reamber.base.Bpm import Bpm


@dataclass
class QuaBpm(Bpm):
    def as_dict(self) -> Dict:
        """ Used to facilitate exporting as Qua from YAML """
        return {
            "StartTime": self.offset,
            "Bpm": self.bpm
        }

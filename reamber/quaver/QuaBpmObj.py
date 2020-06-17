from reamber.base.BpmObj import BpmObj
from dataclasses import dataclass
from typing import Dict


@dataclass
class QuaBpmObj(BpmObj):
    def asDict(self) -> Dict:
        """ Used to facilitate exporting as Qua from YAML """
        return {
            "StartTime": self.offset,
            "Bpm": self.bpm
        }

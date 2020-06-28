from reamber.base.Timed import Timed
from dataclasses import dataclass
from typing import Dict


@dataclass
class QuaSv(Timed):
    multiplier: float = 1.0

    def asDict(self) -> Dict:
        """ Used to facilitate exporting as Qua from YAML """
        return {"StartTime": self.offset,
                "Multiplier": self.multiplier}

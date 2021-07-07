from dataclasses import dataclass
from typing import Dict

from reamber.base.Timed import Timed


@dataclass
class QuaSv(Timed):
    multiplier: float = 1.0

    def as_dict(self) -> Dict:
        """ Used to facilitate exporting as Qua from YAML """
        return {"StartTime": self.offset,
                "Multiplier": self.multiplier}

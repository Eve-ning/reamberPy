from reamber.quaver.QuaNoteMeta import QuaNoteMeta
from reamber.base.Hold import Hold
from dataclasses import dataclass
from typing import Dict


@dataclass
class QuaHold(QuaNoteMeta, Hold):
    def asDict(self) -> Dict:
        """ Used to facilitate exporting as Qua from YAML """
        return {
            'StartTime': self.offset,
            'EndTime': self.offset + self.length,
            'Lane': self.column + 1,
            'KeySounds': self.keySounds
        }

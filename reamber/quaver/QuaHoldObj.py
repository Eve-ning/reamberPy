from reamber.quaver.QuaNoteObjMeta import QuaNoteObjMeta
from reamber.base.HoldObj import HoldObj
from dataclasses import dataclass
from typing import Dict


@dataclass
class QuaHoldObj(QuaNoteObjMeta, HoldObj):
    def asDict(self) -> Dict:
        """ Used to facilitate exporting as Qua from YAML """
        return {
            'StartTime': self.offset,
            'EndTime': self.offset + self.length,
            'Lane': self.column + 1,
            'KeySounds': self.keySounds
        }

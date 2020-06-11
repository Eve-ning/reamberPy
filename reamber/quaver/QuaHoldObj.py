from reamber.quaver.QuaNoteObjMeta import QuaNoteObjMeta
from reamber.base.HoldObj import HoldObj
from dataclasses import dataclass


@dataclass
class QuaHoldObj(QuaNoteObjMeta, HoldObj):
    def asDict(self):
        return {
            'StartTime': self.offset,
            'EndTime': self.offset + self.length,
            'Lane': self.column + 1,
            'KeySounds': self.keySounds
        }

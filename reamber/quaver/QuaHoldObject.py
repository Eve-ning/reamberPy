from reamber.quaver.QuaNoteObjectMeta import QuaNoteObjectMeta
from reamber.base.HoldObject import HoldObject
from dataclasses import dataclass


@dataclass
class QuaHoldObject(QuaNoteObjectMeta, HoldObject):
    def asDict(self):
        return {
            'StartTime': self.offset,
            'EndTime': self.offset + self.length,
            'Lane': self.column + 1,
            'KeySounds': self.keySounds
        }

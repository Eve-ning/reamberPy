from reamber.quaver.QuaNoteMeta import QuaNoteMeta
from reamber.base.Hold import Hold, HoldTail
from dataclasses import dataclass, field
from typing import Dict


@dataclass
class QuaHoldTail(QuaNoteMeta, HoldTail):
    pass

@dataclass
class QuaHold(QuaNoteMeta, Hold):

    _tail: QuaHoldTail = field(init=False)

    def _upcastTail(self, **kwargs) -> QuaHoldTail:
        return QuaHoldTail(**kwargs)

    def asDict(self) -> Dict:
        """ Used to facilitate exporting as Qua from YAML """
        return {
            'StartTime': self.offset,
            'EndTime': self.offset + self.length,
            'Lane': self.column + 1,
            'KeySounds': self.keySounds
        }

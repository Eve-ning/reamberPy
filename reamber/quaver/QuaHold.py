from dataclasses import dataclass, field
from typing import Dict

from reamber.base.Hold import Hold, HoldTail
from reamber.quaver.QuaNoteMeta import QuaNoteMeta


@dataclass
class QuaHoldTail(QuaNoteMeta, HoldTail):
    pass

@dataclass
class QuaHold(QuaNoteMeta, Hold):

    _tail: QuaHoldTail = field(init=False)

    def _upcastTail(self, **kwargs) -> QuaHoldTail:
        return QuaHoldTail(**kwargs)

    def asDict(self, compatible:bool = True) -> Dict:
        """ Used to facilitate exporting as Qua from YAML

        :param compatible: If true, the offsets will be coerced as int for Quaver compatibility.
        """
        return {
            'StartTime': int(self.offset) if compatible else self.offset,
            'EndTime': int(self.offset + self.length) if compatible else self.offset + self.length,
            'Lane': self.column + 1,
            'KeySounds': self.keySounds
        }

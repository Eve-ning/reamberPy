from dataclasses import dataclass
from typing import Dict

from reamber.base.HitObject import HitObject
from reamber.quaver.QuaNoteObjectMeta import QuaNoteObjectMeta


@dataclass
class QuaHitObject(QuaNoteObjectMeta, HitObject):
    def asDict(self) -> Dict:
        return {'StartTime': self.offset,
                'Lane': self.column + 1,
                'KeySounds': self.keySounds}

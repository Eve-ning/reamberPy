from reamber.quaver.QuaNoteObjectMeta import QuaNoteObjectMeta
from reamber.base.HitObject import HitObject
from dataclasses import dataclass, field
from typing import Dict


@dataclass
class QuaHitObject(QuaNoteObjectMeta, HitObject):
    def asDict(self) -> Dict:
        return {'StartTime': self.offset,
                'Lane': self.column + 1,
                'KeySounds': self.keySounds}

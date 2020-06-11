from dataclasses import dataclass
from typing import Dict

from reamber.base.HitObj import HitObj
from reamber.quaver.QuaNoteObjMeta import QuaNoteObjMeta


@dataclass
class QuaHitObj(QuaNoteObjMeta, HitObj):
    def asDict(self) -> Dict:
        return {'StartTime': self.offset,
                'Lane': self.column + 1,
                'KeySounds': self.keySounds}

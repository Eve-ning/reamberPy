from dataclasses import dataclass
from typing import Dict

from reamber.base.Hit import Hit
from reamber.quaver.QuaNoteMeta import QuaNoteMeta


@dataclass
class QuaHit(QuaNoteMeta, Hit):
    def asDict(self) -> Dict:
        """ Used to facilitate exporting as Qua from YAML """
        return {'StartTime': self.offset,
                'Lane': self.column + 1,
                'KeySounds': self.keySounds}

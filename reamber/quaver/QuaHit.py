from dataclasses import dataclass
from typing import Dict

from reamber.base.Hit import Hit
from reamber.quaver.QuaNoteMeta import QuaNoteMeta


@dataclass
class QuaHit(QuaNoteMeta, Hit):
    def as_dict(self, compatible:bool = True) -> Dict:
        """ Used to facilitate exporting as Qua from YAML

        :param compatible: If true, the offset will be coerced as int for Quaver compatibility.
        """
        return {'StartTime': int(self.offset) if compatible else self.offset,
                'Lane': self.column + 1,
                'KeySounds': self.key_sounds}

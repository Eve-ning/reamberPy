from typing import Dict, List, Any

import pandas as pd

from reamber.base import item_props
from reamber.base.Hold import Hold
from reamber.quaver.QuaNoteMeta import QuaNoteMeta


@item_props()
class QuaHold(QuaNoteMeta, Hold):

    def __init__(self, offset: float, column: int, length: float,
                 keysounds: List[str], **kwargs):
        super().__init__(offset=offset, column=column, length=length,
                         keysounds=keysounds, **kwargs)

    def to_yaml(self) -> Dict[str, Any]:
        return dict(StartTime=int(self.offset),
                    EndTime=int(self.tail_offset),
                    Lane=int(self.column + 1),
                    KeySounds=self.keysounds)

    @staticmethod
    def from_yaml(d: Dict[str, Any]):
        s = pd.Series(
            dict(offset=d.get('StartTime', 0),
                 column=d.get('Lane', 1) - 1,
                 keysounds=d.get('KeySounds', []),
                 length=d.get('EndTime', 0) - d.get('StartTime', 0))
        )
        return QuaHold.from_series(s)

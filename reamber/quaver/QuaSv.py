from typing import Dict, Any

import pandas as pd

from reamber.base import item_props
from reamber.base.Timed import Timed


@item_props()
class QuaSv(Timed):
    _props = dict(multiplier=['float', 1.0])

    def __init__(self, offset: float, multiplier: float = 1.0, **kwargs):
        super().__init__(offset=offset, multiplier=multiplier, **kwargs)

    def to_yaml(self) -> Dict:
        """Used to facilitate exporting as Qua from YAML"""
        return dict(StartTime=int(self.offset),
                    Multiplier=float(self.multiplier))

    @staticmethod
    def from_yaml(d: Dict[str, Any]):
        s = pd.Series(dict(offset=d.get('StartTime', 0),
                           multiplier=d.get('Multiplier', 0)))
        return QuaSv.from_series(s)

from typing import Dict, Any

import pandas as pd

from reamber.base import item_props
from reamber.base.Bpm import Bpm


@item_props()
class QuaBpm(Bpm):

    def to_yaml(self):
        return dict(StartTime=int(self.offset), Bpm=float(self.bpm))

    @staticmethod
    def from_yaml(d: Dict[str, Any]):
        s = pd.Series(
            dict(offset=d.get('StartTime', 0), bpm=d.get('Bpm', 120))
        )
        return QuaBpm.from_series(s)

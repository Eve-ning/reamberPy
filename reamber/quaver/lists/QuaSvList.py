from __future__ import annotations

from typing import List, Dict, Any

import pandas as pd

from reamber.base.Property import list_props
from reamber.base.lists.TimedList import TimedList
from reamber.quaver.QuaSv import QuaSv


@list_props(QuaSv)
class QuaSvList(TimedList[QuaSv]):
    @staticmethod
    def from_yaml(dicts: List[Dict[str, Any]]) -> QuaSvList:
        df = pd.DataFrame(dicts)
        df = df.rename(dict(StartTime='offset', Multiplier='multiplier'),
                       axis=1)
        df = df.reindex(df.columns.union(['offset', 'multiplier'], sort=False),
                        axis=1)
        df.offset = df.offset.fillna(0)
        df.multiplier = df.multiplier.fillna(120)
        return QuaSvList(df)

    def to_yaml(self):
        df = self.df.copy()
        return (
            df.astype(
                dict(offset=int, multiplier=float)
            ).rename(
                dict(offset='StartTime', multiplier='Multiplier'), axis=1
            ).to_dict('records')
        )

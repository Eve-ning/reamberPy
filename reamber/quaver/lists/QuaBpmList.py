from __future__ import annotations

from typing import List, Dict, Any

import pandas as pd

from reamber.base.Property import list_props
from reamber.base.lists.BpmList import BpmList
from reamber.quaver.QuaBpm import QuaBpm
from reamber.quaver.lists.QuaTimedList import QuaTimedList


@list_props(QuaBpm)
class QuaBpmList(BpmList[QuaBpm], QuaTimedList[QuaBpm]):

    @staticmethod
    def from_yaml(dicts: List[Dict[str, Any]]) -> QuaBpmList:
        df = pd.DataFrame(dicts)
        df = df.rename(dict(StartTime='offset', Bpm='bpm'), axis=1)
        df = df.reindex(df.columns.union(['offset', 'bpm'], sort=False),
                        axis=1)
        df.offset = df.offset.fillna(0)
        df.bpm = df.bpm.fillna(120)
        return QuaBpmList(df)

    def to_yaml(self):
        return self.df.astype(dict(offset=int, bpm=float)) \
            .rename(dict(offset='StartTime', bpm='Bpm'), axis=1) \
            .drop('metronome', axis=1).to_dict('records')

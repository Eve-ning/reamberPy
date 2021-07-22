from __future__ import annotations

from typing import List, Dict, Any, TypeVar

import pandas as pd

from reamber.base.Property import list_props
from reamber.base.lists import TimedList
from reamber.base.lists.BpmList import BpmList
from reamber.quaver.QuaBpm import QuaBpm

Item = TypeVar('Item')

class QuaTimedList(TimedList[Item]):

    def to_yaml(self):
        """ Used to facilitate exporting as Qua from YAML """
        return [b.to_yaml() for b in self]

    @staticmethod
    def from_yaml(dicts: List[Dict[str, Any]]) -> QuaTimedList:
        df = pd.DataFrame(dicts)
        df = df.rename(dict(StartTime='offset', Bpm='bpm'), axis=1)
        df = df.reindex(df.columns.union(['offset', 'bpm'], sort=False), axis=1)
        df.offset = df.offset.fillna(0)
        df.bpm = df.bpm.fillna(120)
        return QuaTimedList(df)


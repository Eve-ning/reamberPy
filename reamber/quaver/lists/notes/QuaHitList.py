from __future__ import annotations

from typing import List, Dict, Any

import pandas as pd

from reamber.base.Property import list_props
from reamber.base.lists.notes.HitList import HitList
from reamber.quaver.QuaHit import QuaHit
from reamber.quaver.lists.notes.QuaNoteList import QuaNoteList

@list_props(QuaHit)
class QuaHitList(HitList[QuaHit], QuaNoteList[QuaHit]):
    @staticmethod
    def read(dicts: List[Dict[str, Any]]) -> QuaHitList:
        df = pd.DataFrame(dicts)
        df = df.rename(dict(StartTime='offset', Lane='column', KeySounds='keysounds'),
                       axis=1)
        df = df.reindex(df.columns.union(['offset', 'column', 'keysounds'], sort=False), axis=1)
        df.offset = df.offset.fillna(0)
        df.column = df.column.fillna(0)
        df.loc[df.keysounds.isnull(), 'keysounds'] = [ [[]] * df.keysounds.isnull().sum()]
        return QuaHitList(df)

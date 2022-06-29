from __future__ import annotations

from typing import Dict, List

import pandas as pd

from reamber.base.Property import list_props
from reamber.base.lists.notes.HoldList import HoldList
from reamber.quaver.QuaHold import QuaHold
from reamber.quaver.lists.notes.QuaNoteList import QuaNoteList


@list_props(QuaHold)
class QuaHoldList(HoldList[QuaHold], QuaNoteList[QuaHold]):

    @staticmethod
    def from_yaml(dicts: List[Dict[str]]) -> QuaHoldList:
        df = pd.DataFrame(dicts)
        df['EndTime'] -= df['StartTime']
        df = df.rename(
            dict(StartTime='offset',
                 Lane='column',
                 KeySounds='keysounds',
                 EndTime='length'),
            axis=1
        )
        df.column -= 1
        df = df.reindex(
            df.columns.union(
                ['offset', 'column', 'keysounds', 'length'],
                sort=False
            ),
            axis=1
        )
        df.offset = df.offset.fillna(0)
        df.column = df.column.fillna(0)
        df.length = df.length.fillna(0)
        return QuaHoldList(df)

    def to_yaml(self):
        df = self.df.copy()
        df['EndTime'] = df['offset'] + df['length']
        df = df.drop('length', axis=1)
        df.column += 1
        return (
            df.astype(
                dict(offset=int, column=int, EndTime=int)
            ).rename(
                dict(offset='StartTime', column='Lane', keysounds='KeySounds'),
                axis=1
            ).to_dict('records')
        )

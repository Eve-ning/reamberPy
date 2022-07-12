from dataclasses import dataclass, field
from typing import Type, TypeVar

import numpy as np
import pandas as pd

from reamber.base.Map import Map
from reamber.base.lists.notes.HitList import HitList
from reamber.base.lists.notes.HoldList import HoldList
from reamber.osu.OsuMap import OsuMap
from tests.conftest import MAPS_DIR

MapType = TypeVar('MapType', bound=Map)


class LNHeadHandler:
    @staticmethod
    def to_next(holds: list, offset, column, diff_next, *_):
        holds += dict(offset=offset, column=column, length=diff_next)

    @staticmethod
    def default(holds: list, offset, column, length):
        holds += dict(offset=offset, column=column, length=length)


class LNTailHandler:
    @staticmethod
    def to_next(holds: list, offset, column, diff, *_):
        holds += dict(offset=offset, column=column, length=diff)

    @staticmethod
    def default(*_):
        ...


class HitHandler:
    @staticmethod
    def to_next(offset, column, diff, *_):
        return dict(offset=offset, column=column, length=diff)

    @staticmethod
    def default(*_):
        ...

@dataclass
class Inverse:
    hits: list = field(default_factory=list, init=False)
    holds: list = field(default_factory=list, init=False)

    def ln_tail_handler(self, offset, column, length, diff):
        pass

    def ln_head_handler(self, offset, column, length, diff, diff_next):
        self.holds.append(
            dict(offset=offset, column=column, length=diff_next)
        )

    def hit_handler(self, offset, column, diff):
        if np.isnan(diff):
            self.hits.append(dict(offset=offset, column=column))
        else:
            self.holds.append(dict(offset=offset, column=column, length=diff))

    def invert(self,
               m: MapType,
               HoldListType: Type[HoldList],
               HitListType: Type[HitList]) -> MapType:
        df_hits = m.hits.df.loc[:, ['offset', 'column']].assign(is_ln=False)
        df_holds = (
            m.holds.df.loc[:, ['offset', 'column', 'length']]
                .assign(tail_offset=lambda x: x.offset + x.length)
                .rename({'offset': 'offset_'}, axis=1)
                .melt(['column', 'length'], ['offset_', 'tail_offset'],
                      value_name='offset')
                .drop(['variable'], axis=1)
                .assign(is_ln=True)
        )

        dfgs = pd.concat([df_hits, df_holds]) \
            .sort_values(['offset']).groupby('column')

        for _, dfg in dfgs:
            is_ln_head = False

            dfg['diff'] = dfg['offset'].diff().shift(-1)
            ar = dfg.loc[dfg.is_ln, 'diff'].fillna(0).to_numpy()
            ar[::2] += ar[1::2]
            dfg.loc[dfg.is_ln, 'diff_next'] = ar

            for offset, column, is_ln, length, diff, diff_next in \
                dfg.itertuples(index=False):
                if is_ln_head and is_ln:
                    self.ln_tail_handler(offset, column, length, diff)
                elif is_ln:
                    self.ln_head_handler(offset, column, length, diff,
                                         diff_next)
                else:
                    self.hit_handler(offset, column, diff)

                is_ln_head = is_ln

        m.holds = HoldListType.from_dict(self.holds)
        m.hits = HitListType.from_dict(self.hits)
        return m


Inverse().invert(OsuMap.read_file(MAPS_DIR / 'osu/Stella.osu'))

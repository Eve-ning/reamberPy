from dataclasses import dataclass, field
from typing import TypeVar, Callable

import numpy as np
import pandas as pd

from reamber.base.Map import Map

MapType = TypeVar('MapType', bound=Map)


class LNHeadHandler:
    @staticmethod
    def to_next(holds: list, offset, column, diff_next, **_):
        holds.append(dict(offset=offset, column=column, length=diff_next))

    @staticmethod
    def default(holds: list, offset, column, length, **_):
        holds.append(dict(offset=offset, column=column, length=length))


class LNTailHandler:
    @staticmethod
    def to_next(holds: list, offset, column, diff, **_):
        holds.append(dict(offset=offset, column=column, length=diff))

    @staticmethod
    def default(**_):
        ...


class HitHandler:
    @staticmethod
    def to_next(holds: list, offset, column, diff, **_):
        holds.append(dict(offset=offset, column=column, length=diff))

    @staticmethod
    def default(hits: list, offset, column, **_):
        hits.append(dict(offset=offset, column=column))


@dataclass
class Inverse:
    ln_tail_handler: Callable
    ln_head_handler: Callable
    hit_handler: Callable
    hits: list = field(default_factory=list, init=False)
    holds: list = field(default_factory=list, init=False)

    def invert(self, m: MapType, ) -> MapType:
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
                kwargs = dict(
                    hits=self.hits, holds=self.holds,
                    offset=offset, column=column, is_ln=is_ln,
                    length=length, diff=diff, diff_next=diff_next
                )
                is_last_note = np.isnan(diff)
                if is_ln_head and is_ln:
                    self.ln_tail_handler(**kwargs) if is_last_note \
                        else LNTailHandler.default(**kwargs)
                elif is_ln:
                    self.ln_head_handler(**kwargs) if is_last_note \
                        else LNHeadHandler.default(**kwargs)
                else:
                    self.hit_handler(**kwargs) if is_last_note \
                        else HitHandler.default(**kwargs)

                is_ln_head = is_ln

        m.holds = type(m.holds).from_dict(self.holds)
        m.hits = type(m.hits).from_dict(self.hits)
        return m

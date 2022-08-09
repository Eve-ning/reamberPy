from typing import TypeVar

import numpy as np

from reamber.base.Map import Map
from reamber.base.lists.notes.HitList import HitList
from reamber.base.lists.notes.HoldList import HoldList

MapType = TypeVar('MapType', bound=Map)


def full_ln(m: MapType,
            gap: float = 150,
            ln_as_hit_thres: float = 100) -> MapType:
    """ Makes map Full LN

    Args:
        m: Map to make Full LN
        gap: Gap between a HoldTail and the next Note
        ln_as_hit_thres: Threshold before an ln is converted to a hit.
    """

    m = m.deepcopy()
    df = m.stack((HitList, HoldList))._stacked
    dfgs = df.loc[:, ['offset', 'column', 'length']] \
        .sort_values(['offset']).groupby('column')

    holds = []
    hits = []
    # For each column, we populate self.hits and holds for from_dict init.
    for _, dfg in dfgs:
        dfg['diff'] = dfg['offset'].diff().shift(-1)

        for offset, column, length, diff in dfg.itertuples(index=False):
            inv_length = diff - gap
            if np.isnan(diff):
                if np.isnan(length):
                    hits.append(dict(offset=offset, column=column))
                else:
                    holds.append(dict(
                        offset=offset, column=column, length=length
                    ))
                continue
            if inv_length >= ln_as_hit_thres:
                holds.append(dict(
                    offset=offset, column=column, length=inv_length
                ))
            else:
                hits.append(dict(offset=offset, column=column))

    m.hits = type(m.hits).from_dict(hits)
    m.holds = type(m.holds).from_dict(holds)
    return m

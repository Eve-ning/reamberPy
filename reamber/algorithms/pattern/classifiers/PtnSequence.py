""" This will look for a sequence in length pivoting off PtnChord.

This will be useful to look for patterns like jumpstreams vs handstreams where
they will follow a 2 1 2 1 2 ..., 3 1 2 1 3 ... sequence

As the pattern gets more complex it'll be harder to classify them, hence we'll give a broad api on how this can be
detected.

"""

from typing import List
import numpy as np
from dataclasses import dataclass

@dataclass
class PtnPair:
    first: np.ndarray
    second: np.ndarray
    diff: float

class PtnSeqFrame:
    def __init__(self):
        pass


class PtnSequence:

    def __init__(self, groups: List[np.ndarray]):
        self.groups = groups
        self.pairs = []
        for i, j in zip(groups[:-1], groups[1:]):
            iOffset = i['offset'].min()
            jOffset = j['offset'].min()
            diff = jOffset - iOffset
            self.pairs.append(PtnPair(first=i, second=j, diff=diff))

    def combinations(self):

        dt = np.dtype([('columnFrom', np.int8),
                       ('columnTo', np.int8),
                       ('offset', np.float_),
                       ('difference', np.float_)])
        comboList:List = []
        for pair in self.pairs:
            combos = np.array(np.meshgrid(pair.first, pair.second)).T.reshape(-1, 2)

            npCombo = np.empty(len(combos), dtype=dt)
            for npc, c in zip(npCombo, combos):
                npc['columnFrom'] = c[0]['column']
                npc['columnTo'] = c[1]['column']
                npc['offset'] = c[0]['offset']
                npc['difference'] = c[1]['offset'] - c[0]['offset']
            comboList.append(npCombo)
        return comboList
    #
    # def jack(self):
    #
    #     dt = np.dtype([('column', np.int8),
    #                    ('offset', np.float_),
    #                    ('difference', np.float_)])
    #     jackList:List = []
    #     for pair in self.pairs:
    #         firstCols = pair.first['column']
    #         secondCols = pair.second['column']
    #         jackCols = np.intersect1d(firstCols, secondCols)
    #         first = pair.first[np.isin(pair.first['column'], jackCols)]
    #         first.sort(order='column')
    #         second = pair.second[np.isin(pair.second['column'], jackCols)]
    #         second.sort(order='column')
    #         jacks = np.empty(len(jackCols), dtype=dt)
    #         for f, s, j in zip(first, second, jacks):
    #             j['column'] = f['column']
    #             j['offset'] = f['offset']
    #             j['difference'] = s['offset'] - f['offset']
    #         jackList.append(jacks)
    #     return jackList
    #     pass
    #
    #
    #
    #     pass
    #
    #
    #

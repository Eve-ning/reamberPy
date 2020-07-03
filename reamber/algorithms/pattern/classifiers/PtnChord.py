from reamber.base.lists.notes.NoteList import NoteList
from reamber.algorithms.pattern.PtnNote import PtnNote
from reamber.algorithms.pattern.PtnGroup import PtnGroup
from typing import List

import numpy as np

class PtnChord:
    def __init__(self, raw: NoteList):
        self.raw = raw

    def classify(self, window=50.0) -> List[List]:
        count = len(self.raw)
        dt = np.dtype([('column', np.int8), ('offset', np.int32), ('marked', np.bool_)])
        data = np.empty(count, dtype=dt)
        data['column'] = self.raw.columns()
        data['offset'] = self.raw.offsets()
        data['marked'] = 0

        groups = []

        for note in data:
            if note['marked'] is np.True_: continue

            # e.g. searchsorted([0,1,2,6,7,9], 3) -> 2
            # From this we can find the indexes where the groups are.
            left = np.searchsorted(data['offset'], note['offset'], side='left')
            right = np.searchsorted(data['offset'], note['offset'] + window, side='right')
            data[left:right]['marked'] = True  # We mark those that are grouped already.
            conf = list(1 - (data[left:right]['offset'] - note['offset']) / window)
            groups.append(PtnGroup(self.raw[left:right], confidence=conf))

        return groups

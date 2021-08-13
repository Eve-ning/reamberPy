import unittest
from typing import List, Dict

import numpy as np

from reamber.base import Bpm, Hit, Hold, Map
from reamber.base.lists import BpmList
from reamber.base.lists.notes import HitList, HoldList
from reamber.base.lists.notes.NoteList import NoteList


class TestMap(unittest.TestCase):
    """ Not much to test here since Bpm is basically Note. """

    # noinspection DuplicatedCode
    def setUp(self) -> None:
        """

        BPM 300: 200ms/beat
        BPM 200: 300ms/beat

        BPM  300                     300                     200               200
        OFF  0     200   400   600   800   1000  1200  1400  1600  1900  2200  2500
        BEAT 0     1     2     3     0     1     2     3     0     1     2     3
        HIT  0     1  2  3  0  1        2  3           0     1           2  3
        HOLD 2-----2  0--0                 1--------1     0--------------------0
                3--3           3--------3
        """

        self.bpm_offsets    = np.asarray([0, 800, 1600, 2500])
        self.bpm_bpms       = np.asarray([300, 300, 200, 200])
        self.bpm_metronomes = np.asarray([4, 4, 3, 5])
        self.hit_offsets    = np.asarray([0, 200, 300, 400, 500, 600, 900, 1000, 1600, 1600, 2200, 2350])
        self.hit_columns    = np.asarray([0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3])
        self.hold_offsets    = np.asarray([0, 100, 300, 600, 1000, 1500])
        self.hold_columns   = np.asarray([2, 3, 0, 3, 1, 0])
        self.hold_lengths   = np.asarray([200, 100, 100, 300, 300, 1000])

        self.bpms = [Bpm(offset=o, bpm=b, metronome=m) for o, b, m in
                     zip(self.bpm_offsets, self.bpm_bpms, self.bpm_metronomes)]

        self.hits = [Hit(offset=o, column=c) for o, c in zip(self.hit_offsets, self.hit_columns)]
        self.holds = [Hold(offset=o, column=c, length=l) for o, c, l in
                      zip(self.hold_offsets, self.hold_columns, self.hold_lengths)]

        self.map = Map()
        self.map.hits = HitList(self.hits)
        self.map.holds = HoldList(self.holds)
        self.map.bpms = BpmList(self.bpms)
        self.map: Map
        self.stack = self.map.stack()

    def test_stack_loc_conditional(self):
        stack = self.stack
        self.assertEqual(0, stack.column[stack.offset < 1000].min())
        stack.loc[stack.offset < 1000, 'column'] += 1
        self.assertEqual(1, stack.column[stack.offset < 1000].min())
        self.assertEqual(0, stack.column[stack.offset >= 1000].min())

    def test_stack_include(self):
        m = self.map
        stack = m.stack(['hits'])
        with self.assertRaises(KeyError):
            _ = stack.length

        stack = m.stack(['holds'])
        _ = stack.length

    def test_stack_multiple(self):
        stack = self.stack
        stack.loc[(stack.column == 0) & (stack.offset > 1000), ['offset', 'length']] *= 2
        self.assertEqual(3200, stack.offset.max())
        self.assertEqual(2000, self.map.stack(['holds']).length.max())



if __name__ == '__main__':
    unittest.main()

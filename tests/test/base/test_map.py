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
        self.hit_offsets    = np.asarray([0, 200, 300, 400, 500, 600, 900, 1000, 1400, 1600, 2200, 2350])
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

    # @profile
    def test_type(self):
        self.assertIsInstance(self.map.objs, Dict)
        self.assertIsInstance(self.map[NoteList], List)
        self.assertIsInstance(self.map[BpmList][0], BpmList)

    # noinspection PyTypeChecker,DuplicatedCode
    def test_offsets(self):
        self.assertListEqual(self.hit_offsets.tolist(), self.map[HitList][0].offset.tolist())
        self.assertListEqual(self.hit_columns.tolist() ,self.map[HitList][0].column.tolist())
        self.assertListEqual(self.hold_offsets.tolist(), self.map[HoldList][0].offset.tolist())
        self.assertListEqual(self.hold_columns.tolist(), self.map[HoldList][0].column.tolist())
        self.assertListEqual(self.hold_lengths.tolist(), self.map[HoldList][0].length.tolist())
        self.assertListEqual((self.hold_offsets + self.hold_lengths).tolist(),
                             self.map[HoldList][0].tail_offset.tolist())

    def test_mutating(self):
        ...
        # Test Deprecated. Favor Stacking.

    def test_rate(self):
        m = self.map.rate(0.5)
        self.assertListEqual((self.hit_offsets * 2).tolist(), m[HitList][0].offset.tolist())
        self.assertListEqual((self.hold_offsets * 2).tolist(), m[HoldList][0].offset.tolist())
        self.assertListEqual((self.hold_offsets * 2 + self.hold_lengths * 2).tolist(),
                             m[HoldList][0].tail_offset.tolist())
        m = self.map.rate(2)
        self.assertListEqual((self.hit_offsets * 0.5).tolist(), m[HitList][0].offset.tolist())
        self.assertListEqual((self.hold_offsets * 0.5).tolist(), m[HoldList][0].offset.tolist())
        self.assertListEqual((self.hold_offsets * 0.5 + self.hold_lengths * 0.5).tolist(),
                             m[HoldList][0].tail_offset.tolist())

    def test_deepcopy(self):
        self.assertIsNot(self.map, self.map.deepcopy())

    # noinspection DuplicatedCode
    def test_stack_mutate(self):
        s = self.map.stack()
        s.column *= 2

        self.assertListEqual((self.hit_columns * 2).tolist(), self.map[HitList][0].column.tolist())
        self.assertListEqual((self.hold_columns * 2).tolist(), self.map[HoldList][0].column.tolist())

        s.bpm *= 2
        self.assertListEqual((self.bpm_bpms * 2).tolist(), self.map[BpmList][0].bpm.tolist())

        s.offset *= 2
        self.assertListEqual((self.hit_offsets * 2).tolist(), self.map[HitList][0].offset.tolist())
        self.assertListEqual((self.hold_offsets * 2).tolist(), self.map[HoldList][0].offset.tolist())
        self.assertListEqual((self.bpm_offsets * 2).tolist(), self.map[BpmList][0].offset.tolist())

        self.map.stack().length *= 2
        self.assertListEqual((self.hold_lengths * 2).tolist(), self.map[HoldList][0].length.tolist())

    def test_empty_handling(self):
        """ This ensures that the uncalled classes are still initialized. """
        m = Map()
        m.hits = HitList([])
        _ = m[HitList]
        _ = m[HoldList]

    # noinspection DuplicatedCode,PyTypeChecker
    def test_indexing(self):
        m = self.map[HitList]
        self.map[HitList] = m

        self.assertListEqual(self.hit_offsets.tolist(), self.map[HitList][0].offset.tolist())
        self.assertListEqual(self.hold_columns.tolist(), self.map[HoldList][0].column.tolist())
        self.assertListEqual(self.hold_lengths.tolist(), self.map[HoldList][0].length.tolist())
        self.assertListEqual((self.hold_offsets + self.hold_lengths).tolist(),
                             self.map[HoldList][0].tail_offset.tolist())

    def test_stack_view_coerce(self):
        m = self.map
        stack = m.stack()
        self.assertEqual(0, stack.column[stack.offset < 1000].min())
        stack.loc[stack.offset < 1000, 'column'] += 1
        self.assertEqual(1, stack.column[stack.offset < 1000].min())
        self.assertEqual(0, stack.column[stack.offset >= 1000].min())


if __name__ == '__main__':
    unittest.main()

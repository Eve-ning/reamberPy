import unittest

import numpy as np
import pandas as pd

from reamber.base import Bpm, Hit, Hold, Map
from reamber.base.lists import BpmList, NotePkg
from reamber.base.lists.notes import HitList, HoldList
from tests.test.profiling import profile


class TestMap(unittest.TestCase):
    """ Not much to test here since Bpm is basically Note. """

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

        self.map = Map(NotePkg(hits=HitList(self.hits), holds=HoldList(self.holds)), BpmList(self.bpms))
        self.map: Map

    # @profile
    def test_type(self):
        self.assertIsInstance(self.map.lists, dict)
        self.assertIsInstance(self.map.offsets, dict)
        self.assertIsInstance(self.map.notes, NotePkg)
        self.assertIsInstance(self.map.bpms, BpmList)

    def test_reference(self):
        self.assertIs(self.map.offsets['hits'], self.map.notes.hits.offsets)
        self.assertIs(self.map.offsets['holds'], self.map.notes.holds.offsets)
        self.assertIs(self.map.offsets['bpms'], self.map.bpms.offsets)

        self.assertIs(self.map['hits'], self.map.notes.hits)
        self.assertIs(self.map['holds'], self.map.notes.holds)
        self.assertIs(self.map['bpms'], self.map.bpms)

    # noinspection PyTypeChecker
    def test_offsets(self):
        self.assertListEqual(self.hit_offsets.tolist(), self.map.notes.hits.offsets.tolist())
        self.assertListEqual(self.hit_columns.tolist() ,self.map.notes.hits.columns.tolist())
        self.assertListEqual(self.hold_offsets.tolist(), self.map.notes.holds.offsets.tolist())
        self.assertListEqual(self.hold_columns.tolist(), self.map.notes.holds.columns.tolist())
        self.assertListEqual(self.hold_lengths.tolist(), self.map.notes.holds.lengths.tolist())
        self.assertListEqual((self.hold_offsets + self.hold_lengths).tolist(),
                             self.map.notes.holds.tail_offsets.tolist())

    def test_mutating(self):
        self.map.notes.columns = {k: v + 1 for k, v in self.map.notes.columns.items()}  # This produces a dict.
        self.map.notes.hits.columns += 1
        self.assertListEqual((self.hit_columns + 2).tolist(), self.map.notes.hits.columns.tolist())
        self.assertListEqual((self.hold_columns + 1).tolist(), self.map.notes.holds.columns.tolist())

        self.map.notes.offsets = {k: v * 2 for k, v in self.map.notes.offsets.items()}  # This produces a dict.
        self.assertListEqual((self.hit_offsets * 2).tolist(), self.map.notes.hits.offsets.tolist())
        self.assertListEqual((self.hold_offsets * 2).tolist(), self.map.notes.holds.offsets.tolist())

        # Note this important case, if we scale offset, we only scale the hold starts
        self.assertListEqual((self.hold_offsets * 2 + self.hold_lengths).tolist(),
                             self.map.notes.holds.tail_offsets.tolist())

        # We have to explicitly scale the lengths too
        self.map.notes.holds.lengths *= 2
        self.assertListEqual((self.hold_offsets * 2 + self.hold_lengths * 2).tolist(),
                             self.map.notes.holds.tail_offsets.tolist())

    def test_ave_bpm(self):
        self.assertEqual(250, self.map.ave_bpm(3200))

    def test_rate(self):
        m = self.map.rate(0.5)
        self.assertListEqual((self.hit_offsets * 2).tolist(), m.notes.hits.offsets.tolist())
        self.assertListEqual((self.hold_offsets * 2).tolist(), m.notes.holds.offsets.tolist())
        self.assertListEqual((self.hold_offsets * 2 + self.hold_lengths * 2).tolist(),
                             m.notes.holds.tail_offsets.tolist())
        m = self.map.rate(2)
        self.assertListEqual((self.hit_offsets * 0.5).tolist(), m.notes.hits.offsets.tolist())
        self.assertListEqual((self.hold_offsets * 0.5).tolist(), m.notes.holds.offsets.tolist())
        self.assertListEqual((self.hold_offsets * 0.5 + self.hold_lengths * 0.5).tolist(),
                             m.notes.holds.tail_offsets.tolist())

    def test_deepcopy(self):
        self.assertIsNot(self.map, self.map.deepcopy())

    def test_stack_mutate(self):
        s = self.map.stack
        s.columns *= 2

        self.assertListEqual((self.hit_columns * 2).tolist(), self.map.notes.hits.columns.tolist())
        self.assertListEqual((self.hold_columns * 2).tolist(), self.map.notes.holds.columns.tolist())

        s.bpms *= 2
        self.assertListEqual((self.bpm_bpms * 2).tolist(), self.map.bpms.bpms.tolist())

        s.offsets *= 2
        self.assertListEqual((self.hit_offsets * 2).tolist(), self.map.notes.hits.offsets.tolist())
        self.assertListEqual((self.hold_offsets * 2).tolist(), self.map.notes.holds.offsets.tolist())
        self.assertListEqual((self.bpm_offsets * 2).tolist(), self.map.bpms.offsets.tolist())

        self.map.stack.lengths *= 2
        self.assertListEqual((self.hold_lengths * 2).tolist(), self.map.notes.holds.lengths.tolist())

    #
    # def test_bpms(self):
    #     self.assertListEqual([300, 300, 200, 200], self.bpm_list.bpms.to_list())
    #
    # def test_bpms_change(self):
    #     self.bpm_list.bpms *= 2
    #     self.assertListEqual([600, 600, 400, 400], self.bpm_list.bpms.to_list())
    #
    # def test_metronome(self):
    #     self.assertListEqual([4, 4, 3, 5], self.bpm_list.metronomes.to_list())
    #
    # def test_metronome_change(self):
    #     self.bpm_list.metronomes += 1
    #     self.assertListEqual([5, 5, 4, 6], self.bpm_list.metronomes.to_list())
    #
    # def test_init_single_and_multiple(self):
    #     """ Tests whether initializing with a single item list is different from a single item """
    #     self.assertTrue(all(BpmList(self.bpms[0:1]) == BpmList(self.bpms[0])))
    #
    # def test_ix_slice(self):
    #     a = self.bpm_list[0:2]
    #     self.assertTrue(isinstance(a, BpmList), msg=f"{type(a)}")
    #     self.assertEqual(2, len(a))
    #     self.assertTrue(all(BpmList(self.bpms[0:2]) == a))
    #
    # def test_ix_bool(self):
    #     a = self.bpm_list[self.bpm_list.metronomes != 4]
    #     self.assertTrue(isinstance(a, BpmList), msg=f"{type(a)}")
    #     self.assertEqual(2, len(a))
    #     self.assertEqual(1600, a[0].offset)
    #     self.assertEqual(2500, a[1].offset)
    #     self.assertEqual(3, a[0].metronome)
    #     self.assertEqual(5, a[1].metronome)
    #
    # def test_empty_handling(self):
    #     # Check if empty initialization works
    #     # noinspection PyTypeChecker
    #     self.assertTrue(all(BpmList([]).bpms == self.bpm_list.between(500, 750).bpms))
    #     # Check if truly empty
    #     self.assertTrue(BpmList([]).df.empty)
    #     self.assertTrue(self.bpm_list.between(500, 750).df.empty)
    #
    # def test_to_timing_map(self):
    #     tm = self.bpm_list.to_timing_map()


if __name__ == '__main__':
    unittest.main()

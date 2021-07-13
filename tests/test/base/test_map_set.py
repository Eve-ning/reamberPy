import unittest

import numpy as np
import pandas as pd

from reamber.base import Bpm, Hit, Hold, Map, MapSet
from reamber.base.lists import BpmList, NotePkg
from reamber.base.lists.notes import HitList, HoldList
from tests.test.profiling import profile


class TestMapSet(unittest.TestCase):
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
        self.hold_offsets   = np.asarray([0, 100, 300, 600, 1000, 1500])
        self.hold_columns   = np.asarray([2, 3, 0, 3, 1, 0])
        self.hold_lengths   = np.asarray([200, 100, 100, 300, 300, 1000])

        self.bpms = [Bpm(offset=o, bpm=b, metronome=m) for o, b, m in
                     zip(self.bpm_offsets, self.bpm_bpms, self.bpm_metronomes)]

        self.hits = [Hit(offset=o, column=c) for o, c in zip(self.hit_offsets, self.hit_columns)]
        self.holds = [Hold(offset=o, column=c, length=l) for o, c, l in
                      zip(self.hold_offsets, self.hold_columns, self.hold_lengths)]

        self.map1 = Map(NotePkg(hits=HitList(self.hits), holds=HoldList(self.holds)), BpmList(self.bpms))
        self.map2 = self.map1.deepcopy()

        self.map_set = MapSet([self.map1, self.map2])

    def test_type(self):
        self.assertIsInstance(self.map_set.maps, list)

    def test_offsets(self):
        self.assertIsInstance(self.map_set.offsets, list)
        self.map_set.offsets *= 2
        for m in self.map_set:
            for _, li in m.lists.items():
                li.offsets *= 2

        self.assertListEqual((self.hit_offsets * 2).tolist(), m.notes.hits.offsets.tolist())
        self.assertListEqual((self.hold_offsets * 2).tolist(), m.notes.holds.offsets.tolist())
        self.assertListEqual((self.hold_offsets * 2 + self.hold_lengths).tolist(),
                             m.notes.holds.tail_offsets.tolist())
        m = self.map.rate(2)
        self.assertListEqual((self.hit_offsets * 0.5).tolist(), m.notes.hits.offsets.tolist())
        self.assertListEqual((self.hold_offsets * 0.5).tolist(), m.notes.holds.offsets.tolist())
        self.assertListEqual((self.hold_offsets * 0.5 + self.hold_lengths * 0.5).tolist(),
                             m.notes.holds.tail_offsets.tolist())
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

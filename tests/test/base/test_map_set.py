import unittest

import numpy as np

from reamber.base import Bpm, Hit, Hold, Map, MapSet
from reamber.base.lists import BpmList
from reamber.base.lists.notes import HitList, HoldList


# noinspection PyTypeChecker,DuplicatedCode
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

        self.map1 = Map()
        self.map1.hits = HitList(self.hits)
        self.map1.holds = HoldList(self.holds)
        self.map1.bpms = BpmList(self.bpms)
        self.map2 = self.map1.deepcopy()

        self.map_set = MapSet([self.map1, self.map2])

    def test_type(self):
        self.assertIsInstance(self.map_set.maps, list)

    def test_stack(self):
        s = self.map_set.stack()

        self.assertListEqual(self.hit_offsets.tolist(), self.map_set.maps[0][HitList][0].offset.tolist())
        self.assertListEqual(self.hit_columns.tolist() ,self.map_set.maps[0][HitList][0].column.tolist())
        self.assertListEqual(self.hold_offsets.tolist(), self.map_set.maps[0][HoldList][0].offset.tolist())
        self.assertListEqual(self.hold_columns.tolist(), self.map_set.maps[0][HoldList][0].column.tolist())
        self.assertListEqual(self.hold_lengths.tolist(), self.map_set.maps[0][HoldList][0].length.tolist())
        self.assertListEqual((self.hold_offsets + self.hold_lengths).tolist(),
                             self.map_set.maps[0][HoldList][0].tail_offset.tolist())
        self.assertListEqual(self.hit_offsets.tolist(), self.map_set.maps[1][HitList][0].offset.tolist())
        self.assertListEqual(self.hit_columns.tolist() ,self.map_set.maps[1][HitList][0].column.tolist())
        self.assertListEqual(self.hold_offsets.tolist(), self.map_set.maps[1][HoldList][0].offset.tolist())
        self.assertListEqual(self.hold_columns.tolist(), self.map_set.maps[1][HoldList][0].column.tolist())
        self.assertListEqual(self.hold_lengths.tolist(), self.map_set.maps[1][HoldList][0].length.tolist())
        self.assertListEqual((self.hold_offsets + self.hold_lengths).tolist(),
                             self.map_set.maps[1][HoldList][0].tail_offset.tolist())

    def test_stack_offset(self):
        s = self.map_set.stack()
        s.offset *= 2
        self.assertListEqual((self.hit_offsets*2).tolist(), self.map_set.maps[0][HitList][0].offset.tolist())
        self.assertListEqual((self.hold_offsets*2).tolist(), self.map_set.maps[0][HoldList][0].offset.tolist())
        self.assertListEqual(((self.hold_offsets*2) + self.hold_lengths).tolist(),
                             self.map_set.maps[0][HoldList][0].tail_offset.tolist())
        self.assertListEqual((self.hit_offsets*2).tolist(), self.map_set.maps[1][HitList][0].offset.tolist())
        self.assertListEqual((self.hold_offsets*2).tolist(), self.map_set.maps[1][HoldList][0].offset.tolist())
        self.assertListEqual(((self.hold_offsets*2) + self.hold_lengths).tolist(),
                             self.map_set.maps[1][HoldList][0].tail_offset.tolist())

    def test_stack_column(self):
        s = self.map_set.stack()
        s.column *= 2
        self.assertListEqual((self.hit_columns*2).tolist() ,self.map_set.maps[0][HitList][0].column.tolist())
        self.assertListEqual((self.hold_columns*2).tolist(), self.map_set.maps[0][HoldList][0].column.tolist())
        self.assertListEqual((self.hit_columns*2).tolist() ,self.map_set.maps[1][HitList][0].column.tolist())
        self.assertListEqual((self.hold_columns*2).tolist(), self.map_set.maps[1][HoldList][0].column.tolist())

    def test_stack_inline(self):
        """ Checks if inline stacking works """
        self.map_set.stack().column *= 2
        self.assertListEqual((self.hit_columns * 2).tolist(),  self.map_set[0][HitList][0].column.tolist())
        self.assertListEqual((self.hold_columns * 2).tolist(), self.map_set[0][HoldList][0].column.tolist())
        self.assertListEqual((self.hit_columns * 2).tolist(),  self.map_set[1][HitList][0].column.tolist())
        self.assertListEqual((self.hold_columns * 2).tolist(), self.map_set[1][HoldList][0].column.tolist())

    def test_rate(self):
        ms = self.map_set.rate(0.5)
        self.assertListEqual((self.hit_offsets*2).tolist(),  ms[0][HitList][0].offset.tolist())
        self.assertListEqual((self.hold_offsets*2).tolist(), ms[0][HoldList][0].offset.tolist())
        self.assertListEqual((self.hold_offsets * 2 + self.hold_lengths * 2).tolist(),
                             ms[0][HoldList][0].tail_offset.tolist())
        self.assertListEqual((self.hit_offsets*2).tolist(),  ms[1][HitList][0].offset.tolist())
        self.assertListEqual((self.hold_offsets*2).tolist(), ms[1][HoldList][0].offset.tolist())
        self.assertListEqual((self.hold_offsets * 2 + self.hold_lengths * 2).tolist(),
                             ms[1][HoldList][0].tail_offset.tolist())

    def test_deepcopy(self):
        ms = self.map_set.deepcopy()
        ms.stack().column *= 2

        self.assertListEqual((self.hit_columns*2).tolist(),  ms[0][HitList][0].column.tolist())
        self.assertListEqual((self.hold_columns*2).tolist(), ms[0][HoldList][0].column.tolist())
        self.assertListEqual((self.hit_columns*2).tolist(),  ms[1][HitList][0].column.tolist())
        self.assertListEqual((self.hold_columns*2).tolist(), ms[1][HoldList][0].column.tolist())

        self.assertListEqual(self.hit_columns.tolist(),  self.map_set[0][HitList][0].column.tolist())
        self.assertListEqual(self.hold_columns.tolist(), self.map_set[0][HoldList][0].column.tolist())
        self.assertListEqual(self.hit_columns.tolist(),  self.map_set[1][HitList][0].column.tolist())
        self.assertListEqual(self.hold_columns.tolist(), self.map_set[1][HoldList][0].column.tolist())


if __name__ == '__main__':
    unittest.main()

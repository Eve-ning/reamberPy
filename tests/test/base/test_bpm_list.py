import unittest

import pandas as pd

from reamber.base import Bpm
from reamber.base.lists import BpmList


class TestBpmList(unittest.TestCase):

    def setUp(self) -> None:
        """

        BPM 300: 200ms/beat
        BPM 200: 300ms/beat

        BPM  300                300                 200            200
        OFF  0   200  400  600  800  1000 1200 1400 1600 1900 2200 2500
        BEAT 0   1    2    3    0    1    2    3    0    1    2    3
        """

        self.bpms = [
            Bpm(offset=0, bpm=300, metronome=4),
            Bpm(offset=800, bpm=300, metronome=4),
            Bpm(offset=1600, bpm=200, metronome=3),
            Bpm(offset=2500, bpm=200, metronome=5)
        ]
        self.bpm_list = BpmList(self.bpms)

    # @profile
    def test_type(self):
        self.assertTrue(isinstance(self.bpm_list.df, pd.DataFrame))

    def test_bpms(self):
        self.assertListEqual([300, 300, 200, 200], self.bpm_list.bpm.to_list())

    def test_bpms_change(self):
        self.bpm_list.bpm *= 2
        self.assertListEqual([600, 600, 400, 400], self.bpm_list.bpm.to_list())

    def test_metronome(self):
        self.assertListEqual([4, 4, 3, 5], self.bpm_list.metronome.to_list())

    def test_metronome_change(self):
        self.bpm_list.metronome += 1
        self.assertListEqual([5, 5, 4, 6], self.bpm_list.metronome.to_list())

    def test_init_single_and_multiple(self):
        """ Tests whether initializing with a single item list is different from a single item """
        self.assertTrue(all(BpmList(self.bpms[0:1]) == BpmList(self.bpms[0])))

    def test_ix_slice(self):
        a = self.bpm_list[0:2]
        self.assertTrue(isinstance(a, BpmList), msg=f"{type(a)}")
        self.assertEqual(2, len(a))
        self.assertTrue(all(BpmList(self.bpms[0:2]) == a))

    def test_ix_bool(self):
        a = self.bpm_list[self.bpm_list.metronome != 4]
        self.assertTrue(isinstance(a, BpmList), msg=f"{type(a)}")
        self.assertEqual(2, len(a))
        self.assertEqual(1600, a[0].offset)
        self.assertEqual(2500, a[1].offset)
        self.assertEqual(3, a[0].metronome)
        self.assertEqual(5, a[1].metronome)

    def test_empty_handling(self):
        # Check if empty initialization works
        # noinspection PyTypeChecker
        self.assertTrue(all(BpmList([]).bpm == self.bpm_list.between(500, 750).bpm))
        # Check if truly empty
        self.assertTrue(BpmList([]).df.empty)
        self.assertTrue(self.bpm_list.between(500, 750).df.empty)

    def test_to_timing_map(self):
        tm = self.bpm_list.to_timing_map()

    def test_ave_bpm(self):
        self.assertEqual(250, self.bpm_list.ave_bpm(3200))

    def test_current_bpm(self):
        self.assertEqual(800, self.bpm_list.current_bpm(900).offset)
        self.assertEqual(800, self.bpm_list.current_bpm(800).offset)
        self.assertEqual(800, self.bpm_list.current_bpm(799.999).offset)
        with self.assertRaises(IndexError):
            self.bpm_list.current_bpm(-1)


if __name__ == '__main__':
    unittest.main()

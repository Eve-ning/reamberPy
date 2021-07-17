import unittest

import pandas as pd

from reamber.base.lists import NotePkg
from reamber.osu import OsuBpm, OsuSampleSet as Sample, OsuMap
from tests.test.profiling import profile


class TestOsuMap(unittest.TestCase):

    def setUp(self) -> None:
        self.map = OsuMap.read_file("map.osu")
        pass

    def test_type(self):
        self.assertIsInstance(self.map.notes, NotePkg)

    def test_read_bad(self):
        with self.assertRaises(ValueError):
            OsuBpm.read_string("bad_string")
        with self.assertRaises(ValueError):
            OsuBpm.read_string("")

    def test_read_bad_sv(self):
        with self.assertRaises(ValueError):
            # SV String.
            OsuBpm.read_string("1000,-200,4,2,1,30,0,0")

    def test_read_inf(self):
        with self.assertRaises(ZeroDivisionError):
            OsuBpm.read_string("1000,0,4,2,1,30,1,0")

    def test_write(self):
        bpm = OsuBpm.read_string(self.string)
        self.assertEqual(self.string, bpm.write_string())

    def test_is_timing_point(self):
        self.assertTrue(OsuBpm.is_timing_point("1000,200.0,4,3,1,10,1,1"))
        self.assertFalse(OsuBpm.is_timing_point("1000,200.0,4,3,1,10,0,1"))


if __name__ == '__main__':
    unittest.main()

import unittest

import pandas as pd

from reamber.osu import OsuBpm, OsuSampleSet as Sample


class TestOsuBpm(unittest.TestCase):

    def setUp(self) -> None:
        self.string = "1000,200.0,4,3,1,10,1,1"
        self.bpm = OsuBpm(offset=1000,
                          bpm=300,
                          metronome=4,
                          sample_set=Sample.DRUM,
                          sample_set_index=1,
                          volume=10,
                          kiai=True)

    # @profile
    def test_type(self):
        self.assertIsInstance(self.bpm.data, pd.Series)

    def test_meta(self):
        self.assertEqual(Sample.DRUM, self.bpm.sample_set)
        self.assertEqual(1,           self.bpm.sample_set_index)
        self.assertEqual(10,          self.bpm.volume)
        self.assertEqual(True,        self.bpm.kiai)

    def test_from_series(self):

        bpm = OsuBpm.from_series(
            pd.Series(dict(offset=1000, bpm=300, metronome=4, sample_set=Sample.DRUM, sample_set_index=1,
                           volume=10, kiai=True))
        )
        self.assertEqual(self.bpm, bpm)

    def test_code_to_value(self):
        self.assertListEqual([200, 300, 100], [OsuBpm.code_to_value(v) for v in [300, 200, 600]])
        self.assertListEqual([200, 300, 100], [OsuBpm.value_to_code(v) for v in [300, 200, 600]])

    def test_read(self):
        bpm = OsuBpm.read_string(self.string)
        self.assertEqual(self.bpm, bpm)
        bpm = OsuBpm.read_string("2000.0,300.0,5,3,1,10,1,0")
        self.assertEqual(
            OsuBpm(offset=2000, bpm=200, metronome=5, sample_set=Sample.DRUM, sample_set_index=1,
                   volume=10, kiai=False), bpm)

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

import unittest

import pandas as pd

from reamber.osu import OsuSv, OsuSampleSet as Sample


class TestOsuBpm(unittest.TestCase):

    def setUp(self) -> None:
        self.string = "1000.0,-50.0,4,3,1,10,0,1"
        self.sv = OsuSv(offset=1000,
                        multiplier=2,
                        sample_set=Sample.DRUM,
                        sample_set_index=1,
                        volume=10,
                        kiai=True)

    # @profile
    def test_type(self):
        self.assertIsInstance(self.sv.data, pd.Series)

    def test_meta(self):
        self.assertEqual(2,           self.sv.multiplier)
        self.assertEqual(Sample.DRUM, self.sv.sample_set)
        self.assertEqual(1,           self.sv.sample_set_index)
        self.assertEqual(10,          self.sv.volume)
        self.assertEqual(True,        self.sv.kiai)

    def test_from_series(self):
        sv = OsuSv.from_series(
            pd.Series(dict(offset=1000, multiplier=2, sample_set=Sample.DRUM, sample_set_index=1,
                           volume=10, kiai=True))
        )
        self.assertEqual(self.sv, sv)

    def test_code_to_value(self):
        self.assertListEqual([-100, -200, -50], [OsuSv.code_to_value(v) for v in [1, 0.5, 2.0]])
        self.assertListEqual([-100, -200, -50], [OsuSv.value_to_code(v) for v in [1, 0.5, 2.0]])

    def test_read(self):
        sv = OsuSv.read_string(self.string)
        self.assertEqual(self.sv, sv)
        sv = OsuSv.read_string("2000.0,-200.0,4,0,0,40,0,0")
        self.assertEqual(
            OsuSv(offset=1000, multiplier=0.5, sample_set=Sample.AUTO, sample_set_index=1, volume=40, kiai=False), sv)


    def test_read_bad(self):
        with self.assertRaises(ValueError):
            OsuSv.read_string("bad_string")
        with self.assertRaises(ValueError):
            OsuSv.read_string("")

    def test_read_bad_sv(self):
        with self.assertRaises(ValueError):
            # BPM String.
            OsuSv.read_string("1000,-200,4,2,1,30,1,0")

    def test_read_inf(self):
        with self.assertRaises(ZeroDivisionError):
            OsuSv.read_string("1000,0,4,2,1,30,0,0")

    def test_write(self):
        sv = OsuSv.read_string(self.string)
        self.assertEqual(self.string, sv.write_string())

    def test_is_timing_point(self):
        self.assertTrue(OsuSv.is_slider_velocity("1000.0,200.0,4,3,1,10,0,1"))
        self.assertFalse(OsuSv.is_slider_velocity("1000.0,200.0,4,3,1,10,1,1"))


if __name__ == '__main__':
    unittest.main()

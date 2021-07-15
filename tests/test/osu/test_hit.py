import unittest

import pandas as pd

from reamber.osu import OsuHit, OsuSampleSet as Sample


class TestOsuHit(unittest.TestCase):

    def setUp(self) -> None:
        self.string = "192,192,1000,1,3,2:1:0:10:hitsound.wav"
        self.hit = OsuHit(offset=1000,
                          column=1,
                          hitsound_set=Sample.DRUM,
                          sample_set=Sample.SOFT,
                          addition_set=Sample.NORMAL,
                          custom_set=Sample.AUTO,
                          volume=10,
                          hitsound_file="hitsound.wav")

    # @profile
    def test_type(self):
        self.assertIsInstance(self.hit.data, pd.Series)

    def test_meta(self):
        self.assertEqual(Sample.DRUM,    self.hit.hitsound_set)
        self.assertEqual(Sample.SOFT,    self.hit.sample_set)
        self.assertEqual(Sample.NORMAL,  self.hit.addition_set)
        self.assertEqual(Sample.AUTO,    self.hit.custom_set)
        self.assertEqual(10,             self.hit.volume)
        self.assertEqual("hitsound.wav", self.hit.hitsound_file)

    def test_from_series(self):
        hit = OsuHit.from_series(
            pd.Series(dict(offset=1000, column=1, hitsound_set=Sample.DRUM, sample_set=Sample.SOFT,
                           addition_set=Sample.NORMAL,custom_set=Sample.AUTO, volume=10, hitsound_file="hitsound.wav"))
        )
        self.assertEqual(self.hit, hit)

    def test_x_axis_to_column(self):
        self.assertListEqual([0, 1, 2, 3, 4, 5, 6],
                             [OsuHit.x_axis_to_column(x, 7) for x in [36, 109, 182, 256, 329, 402, 475]])
        self.assertListEqual([0, 1, 2, 3],
                             [OsuHit.x_axis_to_column(x, 4) for x in [64, 192, 320, 448]])

    def test_column_to_x_axis(self):
        self.assertListEqual([36, 109, 182, 256, 329, 402, 475],
                             [OsuHit.column_to_x_axis(x, 7) for x in [0, 1, 2, 3, 4, 5, 6]])
        self.assertListEqual([64, 192, 320, 448],
                             [OsuHit.column_to_x_axis(x, 4) for x in [0, 1, 2, 3]])

    def test_read(self):
        hit = OsuHit.read_string(self.string, keys=4)
        self.assertEqual(self.hit, hit)

    def test_read_bad(self):
        with self.assertRaises(ValueError):
            OsuHit.read_string("bad_string", keys=4)
        with self.assertRaises(ValueError):
            OsuHit.read_string("", keys=4)

    def test_read_bad_hold(self):
        with self.assertRaises(ValueError):
            # Hold String.
            OsuHit.read_string("36,192,1000,128,0,2000:0:0:0:0:", keys=4)

    def test_read_bad_key(self):
        with self.assertRaises(AssertionError):
            OsuHit.read_string(self.string, keys=0)

    def test_write(self):
        hit = OsuHit.read_string(self.string, keys=4)
        self.assertEqual(self.string, hit.write_string(keys=4))

    def test_is_hit(self):
        self.assertTrue(OsuHit.is_hit("64,192,1000,1,0,1:2:3:10:hitsound.wav"))
        self.assertFalse(OsuHit.is_hit("36,192,1000,128,0,2000:0:0:0:0:"))


if __name__ == '__main__':
    unittest.main()

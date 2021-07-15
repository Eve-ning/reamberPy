import unittest

import pandas as pd

from reamber.osu import OsuHold, OsuSampleSet as Sample


class TestOsuHold(unittest.TestCase):

    def setUp(self) -> None:
        self.string = "192,192,1000,128,3,2000:2:1:0:10:hitsound.wav"
        self.hold = OsuHold(offset=1000,
                            column=1,
                            length=1000,
                            hitsound_set=Sample.DRUM,
                            sample_set=Sample.SOFT,
                            addition_set=Sample.NORMAL,
                            custom_set=Sample.AUTO,
                            volume=10,
                            hitsound_file="hitsound.wav")

    # @profile
    def test_type(self):
        self.assertIsInstance(self.hold.data, pd.Series)

    def test_meta(self):
        self.assertEqual(Sample.DRUM,    self.hold.hitsound_set)
        self.assertEqual(Sample.SOFT,    self.hold.sample_set)
        self.assertEqual(Sample.NORMAL,  self.hold.addition_set)
        self.assertEqual(Sample.AUTO,    self.hold.custom_set)
        self.assertEqual(10,             self.hold.volume)
        self.assertEqual("hitsound.wav", self.hold.hitsound_file)

    def test_from_series(self):
        hold = OsuHold.from_series(
            pd.Series(dict(offset=1000, column=1, length=1000, hitsound_set=Sample.DRUM, sample_set=Sample.SOFT,
                           addition_set=Sample.NORMAL,custom_set=Sample.AUTO, volume=10, hitsound_file="hitsound.wav"))
        )
        self.assertEqual(self.hold, hold)

    def test_read(self):
        hold = OsuHold.read_string(self.string, keys=4)
        self.assertEqual(self.hold, hold)

    def test_read_bad(self):
        with self.assertRaises(ValueError):
            OsuHold.read_string("bad_string", keys=4)

    def test_read_bad_hit(self):
        with self.assertRaises(ValueError):
            # Hit String.
            OsuHold.read_string("192,192,1000,1,3,1:2:0:10:hitsound.wav", keys=4)

    def test_write(self):
        hold = OsuHold.read_string(self.string, keys=4)
        self.assertEqual(self.string, hold.write_string(keys=4))

    def test_is_hold(self):
        self.assertTrue(OsuHold.is_hold(self.string))
        self.assertFalse(OsuHold.is_hold("192,192,1000,1,3,1:2:0:10:hitsound.wav"))


if __name__ == '__main__':
    unittest.main()

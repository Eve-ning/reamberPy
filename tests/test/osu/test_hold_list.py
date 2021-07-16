import unittest

import pandas as pd

from reamber.osu import OsuHit, OsuSampleSet as Sample, OsuHold
from reamber.osu.lists.notes import OsuHoldList

S0 = Sample.AUTO
S1 = Sample.NORMAL
S2 = Sample.SOFT
S3 = Sample.DRUM

class TestOsuHitList(unittest.TestCase):

    def setUp(self) -> None:

        self.strings = [
            "64,192,0,128,0,1000:0:0:0:10:hitsound0.wav",
            "192,192,1000,128,1,2000:1:1:1:20:hitsound1.wav",
            "320,192,2000,128,2,3000:2:2:2:30:hitsound2.wav",
            "448,192,3000,128,3,4000:3:3:3:40:hitsound3.wav"
        ]
        self.holds = [
            OsuHold(0,    0, 1000, S0, S0, S0, S0, 10, "hitsound0.wav"),
            OsuHold(1000, 1, 1000, S1, S1, S1, S1, 20, "hitsound1.wav"),
            OsuHold(2000, 2, 1000, S2, S2, S2, S2, 30, "hitsound2.wav"),
            OsuHold(3000, 3, 1000, S3, S3, S3, S3, 40, "hitsound3.wav")
        ]
        self.hold_list = OsuHoldList(self.holds)

    # @profile
    def test_type(self):
        self.assertIsInstance(self.hold_list.df, pd.DataFrame)

    def test_df_names(self):
        self.assertListEqual(
            ['offset', 'column', 'length', 'hitsound_set', 'sample_set', 'addition_set',
             'custom_set', 'volume', 'hitsound_file'], list(self.hold_list.df.columns))

    def test_columns(self):
        self.assertListEqual([0, 1, 2, 3], self.hold_list.column.to_list())

    def test_lengths(self):
        self.assertListEqual([1000, 1000, 1000, 1000], self.hold_list.length.to_list())

    def test_lengths_change(self):
        self.hold_list.length *= 2
        self.assertListEqual([2000, 2000, 2000, 2000], self.hold_list.length.to_list())
        self.assertListEqual([2000, 3000, 4000, 5000], self.hold_list.tail_offset.to_list())

    def test_samples(self):
        self.assertListEqual([S0, S1, S2, S3], self.hold_list.sample_set.to_list())
        self.assertListEqual([S0, S1, S2, S3], self.hold_list.addition_set.to_list())
        self.assertListEqual([S0, S1, S2, S3], self.hold_list.hitsound_set.to_list())
        self.assertListEqual([S0, S1, S2, S3], self.hold_list.custom_set.to_list())

    def test_read(self):
        holds = OsuHoldList.read(self.strings, keys=4)
        self.assertListEqual([0, 1, 2, 3], holds.column.to_list())
        self.assertListEqual([0, 1000, 2000, 3000], holds.offset.to_list())

    def test_write(self):
        holds = OsuHoldList.read(self.strings, keys=4)
        self.assertListEqual(self.strings, holds.write(4))

    def test_empty(self):
        self.assertCountEqual(
            ['offset', 'column', 'length', 'hitsound_set', 'sample_set', 'addition_set',
             'custom_set', 'volume', 'hitsound_file'], list(OsuHoldList([]).df.columns))

if __name__ == '__main__':
    unittest.main()

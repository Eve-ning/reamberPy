import unittest

import pandas as pd

from reamber.osu import OsuHit, OsuSampleSet as Sample
from reamber.osu.lists.notes import OsuHitList

S0 = Sample.AUTO
S1 = Sample.NORMAL
S2 = Sample.SOFT
S3 = Sample.DRUM

class TestOsuHitList(unittest.TestCase):

    def setUp(self) -> None:

        self.strings = [
                "64,192,0,1,0,0:0:0:10:hitsound0.wav",
            "192,192,1000,1,1,1:1:1:20:hitsound1.wav",
            "320,192,2000,1,2,2:2:2:30:hitsound2.wav",
            "448,192,3000,1,3,3:3:3:40:hitsound3.wav"
        ]
        self.hits = [
            OsuHit(0,    0, S0, S0, S0, S0, 10, "hitsound0.wav"),
            OsuHit(1000, 1, S1, S1, S1, S1, 20, "hitsound1.wav"),
            OsuHit(2000, 2, S2, S2, S2, S2, 30, "hitsound2.wav"),
            OsuHit(3000, 3, S3, S3, S3, S3, 40, "hitsound3.wav")
        ]
        self.hit_list = OsuHitList(self.hits)

    # @profile
    def test_type(self):
        self.assertIsInstance(self.hit_list.df, pd.DataFrame)

    def test_df_names(self):
        self.assertListEqual(
            ['offset', 'column', 'hitsound_set', 'sample_set', 'addition_set',
             'custom_set', 'volume', 'hitsound_file'], list(self.hit_list.df.columns))

    def test_columns(self):
        self.assertListEqual([0, 1, 2, 3], self.hit_list.columns.to_list())

    def test_columns_change(self):
        self.hit_list.columns += 1
        self.assertListEqual([1, 2, 3, 4], self.hit_list.columns.to_list())

    def test_samples(self):
        self.assertListEqual([S0, S1, S2, S3], self.hit_list.sample_sets.to_list())
        self.assertListEqual([S0, S1, S2, S3], self.hit_list.addition_sets.to_list())
        self.assertListEqual([S0, S1, S2, S3], self.hit_list.hitsound_sets.to_list())
        self.assertListEqual([S0, S1, S2, S3], self.hit_list.custom_sets.to_list())

    def test_read_editor_string(self):
        hits = OsuHitList.read_editor_string("00:00:100 (100|0, 200|1, 300|2) -")
        self.assertListEqual([0, 1, 2], hits.columns.to_list())
        self.assertListEqual([100, 200, 300], hits.offsets.to_list())

    def test_read(self):
        hits = OsuHitList.read(self.strings, keys=4)
        self.assertListEqual([0, 1, 2, 3], hits.columns.to_list())
        self.assertListEqual([0, 1000, 2000, 3000], hits.offsets.to_list())

    def test_write(self):
        hits = OsuHitList.read(self.strings, keys=4)
        self.assertListEqual(self.strings, hits.write(4))

    def test_empty(self):
        self.assertListEqual(
            ['offset', 'column', 'hitsound_set', 'sample_set', 'addition_set',
             'custom_set', 'volume', 'hitsound_file'], list(OsuHitList([]).df.columns))

    def test_a(self):
        print(vars(OsuHitList))


if __name__ == '__main__':
    unittest.main()

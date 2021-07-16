import unittest

import pandas as pd

from reamber.osu import OsuBpm, OsuSampleSet as Sample
from reamber.osu.lists import OsuBpmList

S0 = Sample.AUTO
S1 = Sample.NORMAL
S2 = Sample.SOFT
S3 = Sample.DRUM

class TestOsuHitList(unittest.TestCase):

    def setUp(self) -> None:

        self.strings = [
            "0,200,4,0,0,10,1,1",
            "1000,200,4,1,0,20,1,1",
            "2000,200,4,2,0,30,1,1",
            "3000,200,4,3,0,40,1,1",
        ]
        self.bpms = [
            OsuBpm(0,    300, 4, S0, 0, 10, True),
            OsuBpm(1000, 300, 4, S1, 0, 20, True),
            OsuBpm(2000, 300, 4, S2, 0, 30, True),
            OsuBpm(3000, 300, 4, S3, 0, 40, True)
        ]
        self.bpm_list = OsuBpmList(self.bpms)

    # @profile
    def test_type(self):
        self.assertIsInstance(self.bpm_list.df, pd.DataFrame)

    def test_df_names(self):
        self.assertCountEqual(
            ['offset', 'column', 'hitsound_set', 'sample_set', 'addition_set',
             'custom_set', 'volume', 'hitsound_file'], list(self.bpm_list.df.columns))

    def test_samples(self):
        self.assertListEqual([S0, S1, S2, S3], self.bpm_list.addition_sets.to_list())
        self.assertListEqual([S0, S1, S2, S3], self.bpm_list.hitsound_sets.to_list())
        self.assertListEqual([S0, S1, S2, S3], self.bpm_list.custom_sets.to_list())

    def test_read(self):
        bpms = OsuBpmList.read(self.strings)
        self.assertListEqual([300, 300, 300, 300], bpms.bpms.to_list())
        self.assertListEqual([0, 1000, 2000, 3000], bpms.offsets.to_list())

    def test_write(self):
        bpms = OsuBpmList.read(self.strings)
        self.assertListEqual(self.strings, bpms.write())

    def test_empty(self):
        for i in self.bpms:
            print(i, type(i))


if __name__ == '__main__':
    unittest.main()

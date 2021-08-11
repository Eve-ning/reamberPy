import unittest

import pandas as pd

from reamber.osu import OsuSampleSet as Sample
from reamber.osu.OsuSv import OsuSv
from reamber.osu.lists import OsuBpmList
from reamber.osu.lists.OsuSvList import OsuSvList

S0 = Sample.AUTO
S1 = Sample.NORMAL
S2 = Sample.SOFT
S3 = Sample.DRUM

class TestOsuSvList(unittest.TestCase):

    def setUp(self) -> None:

        self.strings = [
            "0.0,-200.0,4,0,0,10,0,1",
            "1000.0,-200.0,4,1,0,20,0,1",
            "2000.0,-200.0,4,2,0,30,0,1",
            "3000.0,-200.0,4,3,0,40,0,1",
        ]
        self.svs = [
            OsuSv(0,    0.5, 4, S0, 0, 10, True),
            OsuSv(1000, 0.5, 4, S1, 0, 20, True),
            OsuSv(2000, 0.5, 4, S2, 0, 30, True),
            OsuSv(3000, 0.5, 4, S3, 0, 40, True)
        ]
        self.sv_list = OsuSvList(self.svs)

    # @profile
    def test_type(self):
        self.assertIsInstance(self.sv_list.df, pd.DataFrame)

    def test_df_names(self):
        self.assertCountEqual(
            ['offset', 'multiplier', 'metronome', 'sample_set', 'sample_set_index', 'volume', 'kiai'],
            list(self.sv_list.df.columns))

    def test_samples(self):
        # self.assertListEqual([S0, S1, S2, S3], self.sv_list.addition_set.to_list())
        # self.assertListEqual([S0, S1, S2, S3], self.sv_list.hitsound_set.to_list())
        # self.assertListEqual([S0, S1, S2, S3], self.sv_list.custom_set.to_list())
        ...
    def test_read(self):
        svs = OsuSvList.read(self.strings)
        self.assertListEqual([0.5, 0.5, 0.5, 0.5], svs.multiplier.to_list())
        self.assertListEqual([0, 1000, 2000, 3000], svs.offset.to_list())

    def test_write(self):
        svs = OsuSvList.read(self.strings)
        self.assertListEqual(self.strings, svs.write())
    #
    # def test_empty(self):
    #     for i in self.bpms:
    #         print(i, type(i))


if __name__ == '__main__':
    unittest.main()

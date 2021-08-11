import unittest

from reamber.algorithms.timing.TimingMap import BpmChangeSnap, TimingMap, BpmChange, BpmChangeOffset

# import logging
#
# logging.basicConfig(filename="event.log", filemode="w+", level=logging.DEBUG)

from fractions import Fraction

class TestTimingMap(unittest.TestCase):

    # @profile
    def test_by_snap(self):

        bpm_changes_snap = [
            BpmChangeSnap(bpm=200, measure=0, beat=0, slot=Fraction(0),    beats_per_measure=Fraction(4)),
            BpmChangeSnap(bpm=200, measure=1, beat=0, slot=Fraction(0),    beats_per_measure=Fraction(3)),
            BpmChangeSnap(bpm=300, measure=2, beat=0, slot=Fraction(0),    beats_per_measure=Fraction(3)),
            BpmChangeSnap(bpm=300, measure=3, beat=0, slot=Fraction(0),    beats_per_measure=Fraction(4)),
            BpmChangeSnap(bpm=200, measure=3, beat=1, slot=Fraction(0),    beats_per_measure=Fraction(4)),
            BpmChangeSnap(bpm=300, measure=3, beat=3, slot=Fraction(0),    beats_per_measure=Fraction(4)),
            BpmChangeSnap(bpm=200, measure=4, beat=0, slot=Fraction(0),    beats_per_measure=Fraction(4)),
            BpmChangeSnap(bpm=100, measure=4, beat=1, slot=Fraction(1, 2), beats_per_measure=Fraction(4)),
            BpmChangeSnap(bpm=300, measure=5, beat=0, slot=Fraction(0),    beats_per_measure=Fraction(3)),
        ]
        tm = TimingMap.time_by_snap(initial_offset=100,
                                    bpm_changes_snap=bpm_changes_snap)
        self.assertEqual(
            [BpmChange(bpm=200, beats_per_measure=Fraction(4, 1), offset=100, measure=0, beat=0, slot=Fraction(0, 1)),
             BpmChange(bpm=200, beats_per_measure=Fraction(3, 1), offset=1300.0, measure=1, beat=0, slot=Fraction(0, 1)),
             BpmChange(bpm=300, beats_per_measure=Fraction(3, 1), offset=2200.0, measure=2, beat=0, slot=Fraction(0, 1)),
             BpmChange(bpm=300, beats_per_measure=Fraction(4, 1), offset=2800.0, measure=3, beat=0, slot=Fraction(0, 1)),
             BpmChange(bpm=200, beats_per_measure=Fraction(4, 1), offset=3000.0, measure=3, beat=1, slot=Fraction(0, 1)),
             BpmChange(bpm=300, beats_per_measure=Fraction(4, 1), offset=3600.0, measure=3, beat=3, slot=Fraction(0, 1)),
             BpmChange(bpm=200, beats_per_measure=Fraction(4, 1), offset=3800.0, measure=4, beat=0, slot=Fraction(0, 1)),
             BpmChange(bpm=100, beats_per_measure=Fraction(4, 1), offset=4250.0, measure=4, beat=1, slot=Fraction(1, 2)),
             BpmChange(bpm=300, beats_per_measure=Fraction(3, 1), offset=5750.0, measure=5, beat=0, slot=Fraction(0, 1))],

            tm.bpm_changes)

    # @profile
    def test_by_offset(self):

        bpm_changes_offset = [
            BpmChangeOffset(bpm=200, offset=100.0,  beats_per_measure=Fraction(4, 1)),
            BpmChangeOffset(bpm=200, offset=1300.0, beats_per_measure=Fraction(3, 1)),
            BpmChangeOffset(bpm=300, offset=2200.0, beats_per_measure=Fraction(3, 1)),
            BpmChangeOffset(bpm=300, offset=2800.0, beats_per_measure=Fraction(1, 1)),
            BpmChangeOffset(bpm=200, offset=3000.0, beats_per_measure=Fraction(2, 1)),
            BpmChangeOffset(bpm=300, offset=3600.0, beats_per_measure=Fraction(1, 1)),
            BpmChangeOffset(bpm=200, offset=3800.0, beats_per_measure=Fraction(3, 2)),
            BpmChangeOffset(bpm=100, offset=4250.0, beats_per_measure=Fraction(5, 2)),
            BpmChangeOffset(bpm=300, offset=5750.0, beats_per_measure=Fraction(3, 1))
        ]
        tm = TimingMap.time_by_offset(100, bpm_changes_offset)

        self.assertEqual(
            [BpmChange(bpm=200, beats_per_measure=Fraction(4, 1), offset=100, measure=0, beat=0, slot=Fraction(0, 1)),
            BpmChange(bpm=200, beats_per_measure=Fraction(3, 1), offset=1300.0, measure=1, beat=0, slot=Fraction(0, 1)),
            BpmChange(bpm=300, beats_per_measure=Fraction(3, 1), offset=2200.0, measure=2, beat=0, slot=Fraction(0, 1)),
            BpmChange(bpm=300, beats_per_measure=Fraction(1, 1), offset=2800.0, measure=3, beat=0, slot=Fraction(0, 1)),
            BpmChange(bpm=200, beats_per_measure=Fraction(2, 1), offset=3000.0, measure=4, beat=0, slot=Fraction(0, 1)),
            BpmChange(bpm=300, beats_per_measure=Fraction(1, 1), offset=3600.0, measure=5, beat=0, slot=Fraction(0, 1)),
            BpmChange(bpm=200, beats_per_measure=Fraction(3, 2), offset=3800.0, measure=6, beat=0, slot=Fraction(0, 1)),
            BpmChange(bpm=100, beats_per_measure=Fraction(5, 2), offset=4250.0, measure=7, beat=0, slot=Fraction(0, 1)),
            BpmChange(bpm=300, beats_per_measure=Fraction(3, 1), offset=5750.0, measure=8, beat=0, slot=Fraction(0, 1))],
            tm.bpm_changes)

    def test_real(self):
        tm = TimingMap.time_by_offset(0, [
            BpmChangeOffset(bpm=219.0, beats_per_measure=4.0, offset=0.0),
            BpmChangeOffset(bpm=150.0, beats_per_measure=4.0, offset=0.0),
            BpmChangeOffset(bpm=150.0, beats_per_measure=4.0, offset=1600.0),
            BpmChangeOffset(bpm=150.0, beats_per_measure=5.0, offset=4800.0),
            BpmChangeOffset(bpm=150.0, beats_per_measure=4.0, offset=6800.0),
            BpmChangeOffset(bpm=150.0, beats_per_measure=4.0, offset=8400.0),
            BpmChangeOffset(bpm=219.0, beats_per_measure=Fraction(4, 1), offset=13200.0),
            BpmChangeOffset(bpm=219.0, beats_per_measure=4.0, offset=14295.890410958904),
            BpmChangeOffset(bpm=180.0, beats_per_measure=Fraction(4, 1), offset=24158.904109589042),
            BpmChangeOffset(bpm=180.0, beats_per_measure=4.0, offset=25492.237442922375),
            BpmChangeOffset(bpm=130.0, beats_per_measure=Fraction(1, 1), offset=28158.904109589042),
            BpmChangeOffset(bpm=130.0, beats_per_measure=9.0, offset=28620.442571127503),
            BpmChangeOffset(bpm=142.0, beats_per_measure=Fraction(9, 1), offset=32774.28872497366),
            BpmChangeOffset(bpm=155.0, beats_per_measure=9.0, offset=36577.10562638211),
            BpmChangeOffset(bpm=165.0, beats_per_measure=Fraction(4, 1), offset=40060.97659412405),
            BpmChangeOffset(bpm=175.0, beats_per_measure=Fraction(5, 1), offset=41515.5220486695),
            BpmChangeOffset(bpm=183.0, beats_per_measure=Fraction(4, 1), offset=43229.80776295522),
            BpmChangeOffset(bpm=183.0, beats_per_measure=Fraction(4, 1), offset=44541.283172791285),
            BpmChangeOffset(bpm=195.0, beats_per_measure=4.0, offset=45852.75858262735),
            BpmChangeOffset(bpm=195.0, beats_per_measure=4.0, offset=47083.527813396584),
            BpmChangeOffset(bpm=200.0, beats_per_measure=4.0, offset=48314.29704416582),
            BpmChangeOffset(bpm=205.0, beats_per_measure=4.0, offset=49514.29704416582),
            BpmChangeOffset(bpm=205.0, beats_per_measure=Fraction(1, 48), offset=50685.02875148289),
            BpmChangeOffset(bpm=215.0, beats_per_measure=Fraction(191, 48), offset=50691.1263124585),
            BpmChangeOffset(bpm=219.0, beats_per_measure=4.0, offset=51801.59142873757),
            BpmChangeOffset(bpm=195.0, beats_per_measure=4.0, offset=52897.48183969648),
            BpmChangeOffset(bpm=195.0, beats_per_measure=Fraction(1, 1), offset=54128.25107046571),
            BpmChangeOffset(bpm=219.0, beats_per_measure=Fraction(2, 1), offset=54435.943378158016),
            BpmChangeOffset(bpm=219.0, beats_per_measure=4.0, offset=54983.88858363747),
            BpmChangeOffset(bpm=217.0, beats_per_measure=Fraction(1, 1), offset=72518.13515897993),
            BpmChangeOffset(bpm=205.0, beats_per_measure=Fraction(1, 1), offset=72794.63285483247),
            BpmChangeOffset(bpm=195.0, beats_per_measure=Fraction(1, 1), offset=73087.31578166173),
            BpmChangeOffset(bpm=183.0, beats_per_measure=Fraction(1, 1), offset=73395.00808935404),
            BpmChangeOffset(bpm=183.0, beats_per_measure=4.0, offset=73722.87694181305),
            BpmChangeOffset(bpm=115.0, beats_per_measure=Fraction(2, 1), offset=114378.61464673109),
            BpmChangeOffset(bpm=160.0, beats_per_measure=Fraction(2, 1), offset=115422.09290760066),
            BpmChangeOffset(bpm=195.0, beats_per_measure=Fraction(2, 1), offset=116172.09290760066),
            BpmChangeOffset(bpm=220.0, beats_per_measure=Fraction(2, 1), offset=116787.47752298527),
            BpmChangeOffset(bpm=235.0, beats_per_measure=Fraction(2, 1), offset=117332.93206843981),
            BpmChangeOffset(bpm=255.0, beats_per_measure=Fraction(3, 2), offset=117843.57036631215),
            BpmChangeOffset(bpm=275.0, beats_per_measure=Fraction(1, 2), offset=118196.51154278274),
            BpmChangeOffset(bpm=275.0, beats_per_measure=4.0, offset=118305.60245187365),
            BpmChangeOffset(bpm=300.0, beats_per_measure=Fraction(169, 48), offset=124414.69336096456),
            BpmChangeOffset(bpm=315.0, beats_per_measure=Fraction(23, 48), offset=125118.86002763124),
            BpmChangeOffset(bpm=315.0, beats_per_measure=4.0, offset=125210.12986890107),
            BpmChangeOffset(bpm=315.0, beats_per_measure=Fraction(1, 1), offset=130543.4632022344),
            BpmChangeOffset(bpm=275.0, beats_per_measure=Fraction(1, 1), offset=130733.93939271058),
            BpmChangeOffset(bpm=200.0, beats_per_measure=Fraction(1, 2), offset=130952.12121089241),
            BpmChangeOffset(bpm=130.0, beats_per_measure=Fraction(1, 2), offset=131102.1212108924),
            BpmChangeOffset(bpm=185.0, beats_per_measure=Fraction(2, 1), offset=131332.8904416616),
            BpmChangeOffset(bpm=215.0, beats_per_measure=Fraction(2, 1), offset=131981.53909031025),
            BpmChangeOffset(bpm=230.0, beats_per_measure=Fraction(2, 1), offset=132539.67862519398),
            BpmChangeOffset(bpm=250.0, beats_per_measure=Fraction(2, 1), offset=133061.41775562876),
            BpmChangeOffset(bpm=270.0, beats_per_measure=Fraction(2, 1), offset=133541.41775562876),
            BpmChangeOffset(bpm=285.0, beats_per_measure=Fraction(2, 1), offset=133985.8622000732),
            BpmChangeOffset(bpm=300.0, beats_per_measure=Fraction(2, 1), offset=134406.91483165216),
            BpmChangeOffset(bpm=315.0, beats_per_measure=Fraction(7, 4), offset=134806.91483165216),
            BpmChangeOffset(bpm=5.0, beats_per_measure=Fraction(1, 4), offset=135140.2481649855),
            BpmChangeOffset(bpm=219.0, beats_per_measure=4.0, offset=138140.24816498)
        ])
        pass


if __name__ == '__main__':
    unittest.main()

"""
BpmChangeOffset(bpm=219.0, beats_per_measure=4.0, offset=0.0, measure=0, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=150.0, beats_per_measure=4.0, offset=0.0, measure=0, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=150.0, beats_per_measure=4.0, offset=1600.0, measure=1, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=150.0, beats_per_measure=5.0, offset=4800.0, measure=3, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=150.0, beats_per_measure=4.0, offset=6800.0, measure=4, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=150.0, beats_per_measure=4.0, offset=8400.0, measure=5, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=219.0, beats_per_measure=Fraction(4, 1), offset=13200.0, measure=8, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=219.0, beats_per_measure=4.0, offset=14295.890410958904, measure=9, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=180.0, beats_per_measure=Fraction(4, 1), offset=24158.904109589042, measure=18, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=180.0, beats_per_measure=4.0, offset=25492.237442922375, measure=19, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=130.0, beats_per_measure=Fraction(1, 1), offset=28158.904109589042, measure=21, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=130.0, beats_per_measure=9.0, offset=28620.442571127503, measure=22, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=142.0, beats_per_measure=Fraction(9, 1), offset=32774.28872497366, measure=23, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=155.0, beats_per_measure=9.0, offset=36577.10562638211, measure=24, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=165.0, beats_per_measure=Fraction(4, 1), offset=40060.97659412405, measure=25, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=175.0, beats_per_measure=Fraction(5, 1), offset=41515.5220486695, measure=26, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=183.0, beats_per_measure=Fraction(4, 1), offset=43229.80776295522, measure=27, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=183.0, beats_per_measure=Fraction(4, 1), offset=44541.283172791285, measure=28, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=195.0, beats_per_measure=4.0, offset=45852.75858262735, measure=29, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=195.0, beats_per_measure=4.0, offset=47083.527813396584, measure=30, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=200.0, beats_per_measure=4.0, offset=48314.29704416582, measure=31, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=205.0, beats_per_measure=4.0, offset=49514.29704416582, measure=32, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=205.0, beats_per_measure=Fraction(1, 48), offset=50685.02875148289, measure=33, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=215.0, beats_per_measure=Fraction(191, 48), offset=50691.1263124585, measure=34, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=219.0, beats_per_measure=4.0, offset=51801.59142873757, measure=35, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=195.0, beats_per_measure=4.0, offset=52897.48183969648, measure=36, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=195.0, beats_per_measure=Fraction(1, 1), offset=54128.25107046571, measure=37, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=219.0, beats_per_measure=Fraction(2, 1), offset=54435.943378158016, measure=38, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=219.0, beats_per_measure=4.0, offset=54983.88858363747, measure=39, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=217.0, beats_per_measure=Fraction(1, 1), offset=72518.13515897993, measure=55, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=205.0, beats_per_measure=Fraction(1, 1), offset=72794.63285483247, measure=56, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=195.0, beats_per_measure=Fraction(1, 1), offset=73087.31578166173, measure=57, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=183.0, beats_per_measure=Fraction(1, 1), offset=73395.00808935404, measure=58, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=183.0, beats_per_measure=4.0, offset=73722.87694181305, measure=59, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=115.0, beats_per_measure=Fraction(2, 1), offset=114378.61464673109, measure=90, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=160.0, beats_per_measure=Fraction(2, 1), offset=115422.09290760066, measure=91, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=195.0, beats_per_measure=Fraction(2, 1), offset=116172.09290760066, measure=92, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=220.0, beats_per_measure=Fraction(2, 1), offset=116787.47752298527, measure=93, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=235.0, beats_per_measure=Fraction(2, 1), offset=117332.93206843981, measure=94, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=255.0, beats_per_measure=Fraction(3, 2), offset=117843.57036631215, measure=95, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=275.0, beats_per_measure=Fraction(1, 2), offset=118196.51154278274, measure=96, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=275.0, beats_per_measure=4.0, offset=118305.60245187365, measure=97, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=300.0, beats_per_measure=Fraction(169, 48), offset=124414.69336096456, measure=104, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=315.0, beats_per_measure=Fraction(23, 48), offset=125118.86002763124, measure=105, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=315.0, beats_per_measure=4.0, offset=125210.12986890107, measure=106, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=315.0, beats_per_measure=Fraction(1, 1), offset=130543.4632022344, measure=113, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=275.0, beats_per_measure=Fraction(1, 1), offset=130733.93939271058, measure=114, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=200.0, beats_per_measure=Fraction(1, 2), offset=130952.12121089241, measure=115, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=130.0, beats_per_measure=Fraction(1, 2), offset=131102.1212108924, measure=116, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=185.0, beats_per_measure=Fraction(2, 1), offset=131332.8904416616, measure=117, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=215.0, beats_per_measure=Fraction(2, 1), offset=131981.53909031025, measure=118, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=230.0, beats_per_measure=Fraction(2, 1), offset=132539.67862519398, measure=119, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=250.0, beats_per_measure=Fraction(2, 1), offset=133061.41775562876, measure=120, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=270.0, beats_per_measure=Fraction(2, 1), offset=133541.41775562876, measure=121, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=285.0, beats_per_measure=Fraction(2, 1), offset=133985.8622000732, measure=122, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=300.0, beats_per_measure=Fraction(2, 1), offset=134406.91483165216, measure=123, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=315.0, beats_per_measure=Fraction(7, 4), offset=134806.91483165216, measure=124, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=5.0, beats_per_measure=Fraction(1, 4), offset=135140.2481649855, measure=125, beat=0, slot=Fraction(0, 1)),
BpmChangeOffset(bpm=219.0, beats_per_measure=4.0, offset=138140.2481649855, measure=126, beat=0, slot=Fraction(0, 1))"""

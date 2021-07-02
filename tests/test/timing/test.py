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
            BpmChange(bpm=300, beats_per_measure=Fraction(1, 1), offset=2800.0, measure=3, beat=0, slot=Fraction(0, 1)),
            BpmChange(bpm=200, beats_per_measure=Fraction(2, 1), offset=3000.0, measure=4, beat=0, slot=Fraction(0, 1)),
            BpmChange(bpm=300, beats_per_measure=Fraction(1, 1), offset=3600.0, measure=5, beat=0, slot=Fraction(0, 1)),
            BpmChange(bpm=200, beats_per_measure=Fraction(3, 2), offset=3800.0, measure=6, beat=0, slot=Fraction(0, 1)),
            BpmChange(bpm=100, beats_per_measure=Fraction(5, 2), offset=4250.0, measure=7, beat=0, slot=Fraction(0, 1)),
            BpmChange(bpm=300, beats_per_measure=Fraction(3, 1), offset=5750.0, measure=8, beat=0, slot=Fraction(0, 1))],
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


if __name__ == '__main__':
    unittest.main()

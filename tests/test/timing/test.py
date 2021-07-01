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
            BpmChangeSnap(200, 0, 0, Fraction(4), Fraction(0)),
            BpmChangeSnap(200, 1, 0, Fraction(3), Fraction(0)),
            BpmChangeSnap(300, 2, 0, Fraction(3), Fraction(0)),
            BpmChangeSnap(300, 3, 0, Fraction(4), Fraction(0)),
            BpmChangeSnap(200, 3, 1, Fraction(4), Fraction(0)),
            BpmChangeSnap(300, 3, 3, Fraction(4), Fraction(0)),
            BpmChangeSnap(200, 4, 0, Fraction(4), Fraction(0)),
            BpmChangeSnap(100, 4, 1, Fraction(4), Fraction(1, 2)),
            BpmChangeSnap(300, 5, 0, Fraction(3), Fraction(0)),
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
            BpmChangeOffset(bpm=200, beats_per_measure=Fraction(4, 1), offset=100),
            BpmChangeOffset(bpm=200, beats_per_measure=Fraction(3, 1), offset=1300.0),
            BpmChangeOffset(bpm=300, beats_per_measure=Fraction(3, 1), offset=2200.0),
            BpmChangeOffset(bpm=300, beats_per_measure=Fraction(1, 1), offset=2800.0),
            BpmChangeOffset(bpm=200, beats_per_measure=Fraction(2, 1), offset=3000.0),
            BpmChangeOffset(bpm=300, beats_per_measure=Fraction(1, 1), offset=3600.0),
            BpmChangeOffset(bpm=200, beats_per_measure=Fraction(3, 2), offset=3800.0),
            BpmChangeOffset(bpm=100, beats_per_measure=Fraction(5, 2), offset=4250.0),
            BpmChangeOffset(bpm=300, beats_per_measure=Fraction(3, 1), offset=5750.0)
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

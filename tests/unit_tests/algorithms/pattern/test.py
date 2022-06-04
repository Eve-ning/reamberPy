import unittest

from reamber.algorithms.pattern.filters.PtnFilter import PtnFilterChord, PtnFilterCombo


class TestFilter(unittest.TestCase):

    def test_chord(self):
        a = PtnFilterChord.create(chord_sizes=[[1, 1, 1], [2, 2, 2]], keys=4,
                                  options=PtnFilterChord.Option.AND_HIGHER | PtnFilterChord.Option.ANY_ORDER)

        b = PtnFilterChord.create(chord_sizes=[[2, 2, 2], [3, 3, 3]], keys=4,
                                  options=PtnFilterChord.Option.AND_LOWER | PtnFilterChord.Option.ANY_ORDER)
        c = a & b
        self.assertEqual(c.ar.shape, (27,3))

    def test_combo(self):
        c = PtnFilterCombo.create(combos=[[0, 0, 0], [1, 1, 1]], keys=4)
        d = PtnFilterCombo.create(combos=[[0, 0, 0], [2, 2, 2]], keys=4)
        e = c | d
        self.assertEqual(e.ar.shape, (3,3))


if __name__ == '__main__':
    unittest.main()

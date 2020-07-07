import unittest

from reamber.algorithms.pattern.filters.PtnFilter import PtnFilterChord, PtnFilterCombo


class TestFilter(unittest.TestCase):

    def test_chord(self):
        a = PtnFilterChord.create(sizes=[[1, 1, 1], [2, 2, 2]], keys=4,
                                  method=PtnFilterChord.Method.AND_HIGHER | PtnFilterChord.Method.ANY_ORDER)

        b = PtnFilterChord.create(sizes=[[2, 2, 2], [3, 3, 3]], keys=4,
                                  method=PtnFilterChord.Method.AND_LOWER | PtnFilterChord.Method.ANY_ORDER)
        c = a & b
        self.assertEqual(c.ar.shape, (27,3))

    def test_combo(self):
        c = PtnFilterCombo.create(cols=[[0,0,0], [1,1,1]], keys=4)
        d = PtnFilterCombo.create(cols=[[0,0,0], [2,2,2]], keys=4)
        e = c | d
        self.assertEqual(e.ar.shape, (3,3))


if __name__ == '__main__':
    unittest.main()

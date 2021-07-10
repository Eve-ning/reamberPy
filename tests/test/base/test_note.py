import unittest

import pandas as pd

from reamber.base import Note


class TestNote(unittest.TestCase):
    """ The purpose of this test is to test the architecture of Base. """

    def setUp(self) -> None:
        self.note = Note(offset=1000, column=1)

    # @profile
    def test_type(self):
        self.assertTrue(isinstance(self.note.data, pd.Series))

    # noinspection DuplicatedCode
    def test_eq(self):
        self.assertEqual(Note(offset=1000, column=1), self.note)
        self.assertNotEqual(Note(offset=1000, column=2), self.note)
        self.assertNotEqual(Note(offset=2000, column=1), self.note)
        self.assertNotEqual(Note(offset=2000, column=2), self.note)

    def test_op_gt(self):
        self.assertTrue(self.note < Note(offset=2000, column=1))

    def test_op_lt(self):
        self.assertTrue(self.note > Note(offset=500, column=1))

    def test_deepcopy(self):
        self.assertFalse(self.note is Note(offset=1000, column=1))
        self.assertFalse(self.note is self.note.deepcopy())
        hit = self.note
        self.assertTrue(self.note is hit)

    # noinspection DuplicatedCode
    def test_offset_op(self):
        hit = Note(offset=1000, column=1)
        self.assertEqual(1, hit.column)
        hit.column *= 2
        self.assertEqual(2, hit.column)
        _ = hit.column * 2
        self.assertEqual(2, hit.column)

    def test_sort(self):
        objs = [Note(i, 1) for i in reversed(range(10))]  # [9 -> 0]
        objs.sort()
        self.assertEqual([Note(i, 1) for i in range(10)], objs)

    def test_from_series(self):
        hit = Note.from_series(pd.Series(dict(offset=1000, column=1)))
        self.assertEqual(self.note, hit)

    def test_from_series_excess_args(self):
        hit = Note.from_series(pd.Series(dict(offset=1000, column=1, a=2000)))
        self.assertEqual(self.note, hit)

    def test_from_series_missing_args(self):
        with self.assertRaises(TypeError):
            _ = Note.from_series(pd.Series(dict(offset=1000, a=2000)))

    def test_from_series_no_args(self):
        with self.assertRaises(TypeError):
            _ = Note.from_series(pd.Series(dict(), dtype=object))


if __name__ == '__main__':
    unittest.main()

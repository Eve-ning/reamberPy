import unittest

import pandas as pd
import pytest

from reamber.base import Note


class TestNote():
    """ The purpose of this test is to test the architecture of Base. """

    @pytest.fixture(autouse=True)
    def setUp(self) -> None:
        self.note = Note(offset=1000, column=1)

    # @profile
    def test_type(self):
        assert isinstance(self.note.data, pd.Series)

    # noinspection DuplicatedCode
    def test_eq(self):
        assert (Note(offset=1000, column=1) == self.note)
        assert (Note(offset=1000, column=2) != self.note)
        assert (Note(offset=2000, column=1) != self.note)
        assert (Note(offset=2000, column=2) != self.note)

    def test_op_gt(self):
        assert self.note < Note(offset=2000, column=1)

    def test_op_lt(self):
        assert self.note > Note(offset=500, column=1)

    def test_deepcopy(self):
        assert self.note is not Note(offset=1000, column=1)
        assert self.note is not self.note.deepcopy()
        hit = self.note
        assert self.note is hit

    # noinspection DuplicatedCode
    def test_offset_op(self):
        hit = Note(offset=1000, column=1)
        assert 1 == hit.column
        hit.column *= 2
        assert 2 == hit.column
        _ = hit.column * 2
        assert 2 == hit.column

    def test_sort(self):
        objs = [Note(i, 1) for i in reversed(range(10))]  # [9 -> 0]
        objs.sort()
        assert [Note(i, 1) for i in range(10)] == objs

    def test_from_series(self):
        hit = Note.from_series(pd.Series(dict(offset=1000, column=1)))
        assert self.note == hit

    def test_from_series_excess_args(self):
        hit = Note.from_series(pd.Series(dict(offset=1000, column=1, a=2000)))
        assert self.note == hit

    def test_from_series_missing_args(self):
        with pytest.raises(TypeError):
            _ = Note.from_series(pd.Series(dict(offset=1000, a=2000)))

    def test_from_series_no_args(self):
        with pytest.raises(TypeError):
            _ = Note.from_series(pd.Series(dict(), dtype=object))


if __name__ == '__main__':
    unittest.main()

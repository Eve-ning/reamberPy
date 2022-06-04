import unittest

import pandas as pd

from reamber.base import Hold
from reamber.base.lists.notes.HoldList import HoldList


class TestHoldList(unittest.TestCase):

    def setUp(self) -> None:
        self.holds = [
            Hold(offset=0, column=1, length=500),
            Hold(offset=1000, column=2, length=500),
            Hold(offset=2000, column=3, length=1000),
            Hold(offset=3000, column=4, length=1000)
        ]
        self.hold_list = HoldList(self.holds)

    # @profile
    def test_type(self):
        self.assertTrue(isinstance(self.hold_list.df, pd.DataFrame))

    def test_lengths(self):
        self.assertListEqual([500, 500, 1000, 1000], self.hold_list.length.to_list())

    def test_lengths_change(self):
        self.hold_list.length *= 10
        self.assertListEqual([5000, 5000, 10000, 10000], self.hold_list.length.to_list())
        self.assertListEqual([5000, 6000, 12000, 13000], self.hold_list.tail_offset.to_list())

    def test_offsets(self):
        self.assertListEqual([0, 1000, 2000, 3000], self.hold_list.offset.to_list())
        self.assertListEqual([0, 1000, 2000, 3000], self.hold_list.head_offset.to_list())
        self.assertListEqual([500, 1500, 3000, 4000], self.hold_list.tail_offset.to_list())

    def test_init_single_and_multiple(self):
        """ Tests whether initializing with a single item list is different from a single item """
        self.assertTrue(all(HoldList(self.holds[0:1]) == HoldList(self.holds[0])))

    def test_ix_slice(self):
        a = self.hold_list[0:2]
        self.assertTrue(isinstance(a, HoldList), msg=f"{type(a)}")
        self.assertEqual(2, len(a))
        self.assertTrue(all(HoldList(self.holds[0:2]) == a))

    def test_ix_bool(self):
        a = self.hold_list[self.hold_list.length < 1000]
        self.assertTrue(isinstance(a, HoldList), msg=f"{type(a)}")
        self.assertEqual(2, len(a))
        self.assertEqual(500, a[0].length)
        self.assertEqual(500, a[1].length)
        self.assertEqual(0, a[0].offset)
        self.assertEqual(1000, a[1].offset)

    def test_in_columns(self):
        a = self.hold_list.in_columns([2,3])
        self.assertEqual(2, len(a))
        self.assertEqual(1000, a[0].offset)
        self.assertEqual(2000, a[1].offset)

        # Assert that this is a deepcopy.
        a.iloc[0].offset += 500
        self.assertEqual(1000, self.hold_list[1].offset)
        self.assertEqual(1500, a[0].offset)

    def test_first_last_offset(self):
        self.assertEqual(0, self.hold_list.first_offset())
        self.assertEqual(4000, self.hold_list.last_offset())
        self.assertEqual((0, 4000), self.hold_list.first_last_offset())

    def test_empty_handling(self):
        # Check if empty initialization works
        self.assertTrue(all(HoldList([]).column == self.hold_list.between(500, 750).column))
        # Check if truly empty
        self.assertTrue(HoldList([]).df.empty)
        self.assertTrue(self.hold_list.between(500, 750).df.empty)

    def test_describe(self):
        self.assertIsInstance(self.hold_list.df.describe(), pd.DataFrame)

    def test_rolling(self):
        self.assertDictEqual({0: 1, 1000: 1, 2000: 1, 3000: 1},
                             self.hold_list.rolling_density(1000))
        self.assertDictEqual({0: 1, 500: 1, 1000: 1, 1500: 1, 2000: 1, 2500: 1, 3000: 1, 3500: 0},
                             self.hold_list.rolling_density(1000, 500))
        self.assertDictEqual({0: 1, 500: 0, 1000: 1, 1500: 0, 2000: 1, 2500: 0, 3000: 1, 3500: 0},
                             self.hold_list.rolling_density(500))

    def test_activity(self):
        # noinspection PyTypeChecker
        self.assertListEqual([1000, 1000, 1000, 1000], self.hold_list.activity().tolist())

    def test_between(self):
        """
            0         1000
            [----]    [----]
               500      1500
        """
        # [---------)
        # [----]    [----]
        self.assertTrue(
            (HoldList(self.holds[0]).to_numpy() ==
            self.hold_list.between(0, 1000, include_ends=(True, False), include_head=True, include_tail=False)
            .to_numpy()).all())

        #  [--------)
        # [----]    [----]
        self.assertTrue(
            (HoldList([]).to_numpy() ==
            self.hold_list.between(100, 1000, include_ends=(True, False), include_head=True, include_tail=False)
            .to_numpy()).all())

        #      [----)
        # [----]    [----]
        self.assertTrue(
            (HoldList(self.holds[0]).to_numpy() ==
            self.hold_list.between(500, 1000, include_ends=(True, False), include_head=True, include_tail=True)
            .to_numpy()).all())

        #      (----)
        # [----]    [----]
        self.assertTrue(
            (HoldList([]).to_numpy() ==
            self.hold_list.between(500, 1000, include_ends=(False, False), include_head=True, include_tail=True)
            .to_numpy()).all())

        #      [----]
        # [----]    [----]
        self.assertTrue(
            (HoldList(self.holds[0:2]).to_numpy() ==
            self.hold_list.between(500, 1000, include_ends=(True, True), include_head=True, include_tail=True)
            .to_numpy()).all())

        #      [-----]
        # [----]    [----]
        self.assertTrue(
            (HoldList(self.holds[0]).to_numpy() ==
            self.hold_list.between(500, 1100, include_ends=(True, True), include_head=False, include_tail=True)
            .to_numpy()).all())


if __name__ == '__main__':
    unittest.main()

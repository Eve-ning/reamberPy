import unittest

import pandas as pd

from reamber.base import Hit
from reamber.base.lists.notes.HitList import HitList


class TestHitList(unittest.TestCase):
    """ Not much to test here since Hit is basically Note. """

    def setUp(self) -> None:
        self.hits = [
            Hit(offset=0, column=1),
            Hit(offset=1000, column=2),
            Hit(offset=2000, column=3),
            Hit(offset=3000, column=4)
        ]
        self.hit_list = HitList(self.hits)

    # @profile
    def test_type(self):
        self.assertTrue(isinstance(self.hit_list.df, pd.DataFrame))

    def test_columns(self):
        self.assertListEqual([1, 2, 3, 4], self.hit_list.columns.to_list())

    def test_columns_change(self):
        self.hit_list.columns += 1
        self.assertListEqual([2, 3, 4, 5], self.hit_list.columns.to_list())

    def test_offsets(self):
        self.assertListEqual([0, 1000, 2000, 3000], self.hit_list.offsets.to_list())

    def test_offsets_change(self):
        self.hit_list.offsets *= 10
        self.assertListEqual([0, 10000, 20000, 30000], self.hit_list.offsets.to_list())

    def test_init_single_and_multiple(self):
        """ Tests whether initializing with a single item list is different from a single item """
        self.assertTrue(all(HitList(self.hits[0:1]) == HitList(self.hits[0])))

    def test_ix_slice(self):
        a = self.hit_list[0:2]
        self.assertTrue(isinstance(a, HitList), msg=f"{type(a)}")
        self.assertEqual(2, len(a))
        self.assertTrue(all(HitList(self.hits[0:2]) == a))

    def test_ix_bool(self):
        a = self.hit_list[self.hit_list.offsets < 1500]
        self.assertTrue(isinstance(a, HitList), msg=f"{type(a)}")
        self.assertEqual(2, len(a))
        self.assertEqual(0, a[0].offset)
        self.assertEqual(1000, a[1].offset)
        self.assertEqual(1, a[0].column)
        self.assertEqual(2, a[1].column)

    def test_loc(self):
        a = self.hit_list[0:2]
        b = a.deepcopy()
        b.df.loc[0].offset += 500
        b.df.loc[0, 'offset'] += 750
        self.assertEqual(1250, b.iloc[0].offset)
        self.assertEqual(0, a.iloc[0].offset)

    def test_iloc(self):
        a = self.hit_list[0:2]
        b = a.deepcopy()
        b.df.iloc[0] = 1
        self.assertEqual(1, b.iloc[0].offset)
        self.assertEqual(1, b.iloc[0].column)
        self.assertEqual(0, a.iloc[0].offset)

    def test_in_columns(self):
        a = self.hit_list.in_columns([2,3])
        self.assertEqual(2, len(a))
        self.assertEqual(1000, a[0].offset)
        self.assertEqual(2000, a[1].offset)

        # Assert that this is a deepcopy.
        a.iloc[0].offset += 500
        self.assertEqual(1000, self.hit_list[1].offset)
        self.assertEqual(1500, a[0].offset)

    def test_first_last_offset(self):
        self.assertEqual(0, self.hit_list.first_offset())
        self.assertEqual(3000, self.hit_list.last_offset())
        self.assertEqual((0, 3000), self.hit_list.first_last_offset())

    def test_empty_handling(self):
        # Check if empty initialization works
        self.assertTrue(all(HitList([]).columns == self.hit_list.between(500, 750).columns))
        # Check if truly empty
        self.assertTrue(HitList([]).df.empty)
        self.assertTrue(self.hit_list.between(500, 750).df.empty)

    def test_between(self):
        self.assertTrue(all(HitList(self.hits[0:1]) == self.hit_list.between(0, 1000)))
        self.assertTrue(all(HitList(self.hits[0:1]) == self.hit_list.between(0, 1000, include_ends=(True, False))))
        self.assertTrue(all(HitList(self.hits[0:2]) == self.hit_list.between(0, 1000, include_ends=(True, True))))
        self.assertTrue(self.hit_list.between(0, 1000, include_ends=(False, False)).df.empty)

        # Because the indexes are different it cannot compare, so I cast to numpy.
        self.assertTrue((HitList(self.hits[1:2]).to_numpy() ==
                         self.hit_list.between(0, 1000, include_ends=(False, True)).to_numpy()).all())

    def test_append_timed(self):
        a = self.hit_list.append(self.hits[0])
        self.assertEqual(1, a[-1].column)
        self.assertEqual(5, len(a))

    def test_append_timed_list(self):
        a = self.hit_list.append(self.hit_list)
        self.assertEqual(1, a[-4].column)
        self.assertEqual(2, a[-3].column)
        self.assertEqual(3, a[-2].column)
        self.assertEqual(4, a[-1].column)
        self.assertEqual(8, len(a))

    def test_append_series(self):
        a = self.hit_list.append(self.hits[0].data)
        self.assertEqual(1, a[-1].column)
        self.assertEqual(5, len(a))

    def test_append_df(self):
        a = self.hit_list.append(self.hit_list.df)
        self.assertEqual(1, a[-4].column)
        self.assertEqual(2, a[-3].column)
        self.assertEqual(3, a[-2].column)
        self.assertEqual(4, a[-1].column)
        self.assertEqual(8, len(a))


if __name__ == '__main__':
    unittest.main()

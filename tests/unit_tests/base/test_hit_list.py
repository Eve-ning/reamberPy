import pandas as pd

from reamber.base.lists.notes.HitList import HitList


# @profile
def test_type(hit_list):
    assert isinstance(hit_list.df, pd.DataFrame)


def test_columns(hit_list):
    assert [1, 2, 3, 4] == hit_list.column.to_list()


def test_columns_change(hit_list):
    hit_list.column += 1
    assert [2, 3, 4, 5] == hit_list.column.to_list()


def test_offsets(hit_list):
    assert [0, 1000, 2000, 3000] == hit_list.offset.to_list()


def test_offsets_change(hit_list):
    hit_list.offset *= 10
    assert [0, 10000, 20000, 30000], hit_list.offset.to_list()


def test_init_single_and_multiple(hits):
    """ Tests whether initializing with a single item list is different from a single item """
    assert HitList(hits[0:1]) == HitList(hits[0])


def test_ix_slice(hit_list, hits):
    a = hit_list[0:2]
    assert isinstance(a, HitList)
    assert 2, len(a)
    assert HitList(hits[0:2]) == a


def test_ix_bool(hit_list):
    a = hit_list[hit_list.offset < 1500]
    assert isinstance(a, HitList)
    assert 2 == len(a)
    assert 0 == a[0].offset
    assert 1000 == a[1].offset
    assert 1 == a[0].column
    assert 2 == a[1].column


def test_loc(hit_list):
    a = hit_list[0:2]
    b = a.deepcopy()
    b.df.loc[0].offset += 500
    b.df.loc[0, 'offset'] += 750
    assert 1250 == b.iloc[0].offset
    assert 0 == a.iloc[0].offset


def test_iloc(hit_list):
    a = hit_list[0:2]
    b = a.deepcopy()
    b.df.iloc[0] = 1
    assert 1 == b.iloc[0].offset
    assert 1 == b.iloc[0].column
    assert 0 == a.iloc[0].offset


def test_in_columns(hit_list):
    a = hit_list.in_columns([2, 3])
    assert 2 == len(a)
    assert 1000 == a[0].offset
    assert 2000 == a[1].offset

    # Assert that this is a deepcopy.
    a.iloc[0].offset += 500
    assert 1000 == hit_list[1].offset
    assert 1500 == a[0].offset


def test_first_last_offset(hit_list):
    assert 0 == hit_list.first_offset()
    assert 3000 == hit_list.last_offset()
    assert (0, 3000) == hit_list.first_last_offset()


def test_empty_handling(hit_list):
    # Check if empty initialization works
    assert HitList([]).column == hit_list.between(500, 750).column
    # Check if truly empty
    assert HitList([]).df.empty
    assert hit_list.between(500, 750).df.empty


def test_between(hit_list, hits):
    assert all(HitList(hits[0:1]) ==
               hit_list.between(0, 1000))
    assert all(HitList(hits[0:1]) ==
               hit_list.between(0, 1000, include_ends=(True, False)))
    assert all(HitList(hits[0:2]) ==
               hit_list.between(0, 1000, include_ends=(True, True)))
    assert hit_list.between(0, 1000, include_ends=(False, False)).df.empty

    # Because the indexes are different it cannot compare, so I cast to numpy.
    assert HitList(hits[1:2]).to_numpy() == \
           hit_list.between(0, 1000, include_ends=(False, True)).to_numpy()


def test_append_timed(hit_list, hits):
    a = hit_list.append(hits[0])
    assert 1 == a[-1].column
    assert 5 == len(a)

def test_append_timed_list(hit_list):
    a = hit_list.append(hit_list)
    assert 1 == a[-4].column
    assert 2 == a[-3].column
    assert 3 == a[-2].column
    assert 4 == a[-1].column
    assert 8 == len(a)

def test_append_series(hit_list, hits):
    a = hit_list.append(hits[0].data)
    assert 1 == a[-1].column
    assert 5 == len(a)

def test_append_df(hit_list):
    a = hit_list.append(hit_list.df)
    assert 1 == a[-4].column
    assert 2 == a[-3].column
    assert 3 == a[-2].column
    assert 4 == a[-1].column
    assert 8 == len(a)

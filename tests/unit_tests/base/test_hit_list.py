import numpy as np
import pandas as pd

from reamber.base.lists.notes.HitList import HitList


# @profile
def test_type(hit_list):
    assert isinstance(hit_list.df, pd.DataFrame)


def test_columns(hit_list, columns):
    assert all(columns == hit_list.column.to_list())


def test_columns_change(hit_list, columns):
    hit_list.column += 1
    assert all(columns + 1 == hit_list.column.to_list())


def test_offsets(hit_list, offsets):
    assert all(offsets == hit_list.offset.to_list())


def test_offsets_change(hit_list, offsets):
    hit_list.offset *= 2
    assert all(offsets * 2 == hit_list.offset.to_list())


def test_init_single_and_multiple(hits):
    """ Tests whether initializing with a single item list is different from a single item """
    assert all(HitList(hits[0:1]) == HitList(hits[0]))


def test_ix_slice(hit_list, hits):
    a = hit_list[0:2]
    assert isinstance(a, HitList)
    assert 2 == len(a)
    assert all(HitList(hits[0:2]) == a)


def test_ix_bool(hit_list, offsets, columns):
    a = hit_list[hit_list.offset < offsets[2]]
    assert isinstance(a, HitList)
    assert 2 == len(a)
    assert offsets[0] == a[0].offset
    assert offsets[1] == a[1].offset
    assert columns[0] == a[0].column
    assert columns[1] == a[1].column


def test_loc(hit_list, randintp):
    hit_list.df.loc[0].offset += randintp
    hit_list.df.loc[0, 'offset'] += randintp
    assert randintp * 2 == hit_list.iloc[0].offset


def test_iloc(hit_list, randintp):
    hit_list.df.iloc[0] = randintp
    assert randintp == hit_list.iloc[0].offset
    assert randintp == hit_list.iloc[0].column


def test_in_columns(hit_list, offsets, columns):
    a = hit_list.in_columns(columns[:2])
    assert 2 == len(a)
    assert all(offsets[:2] == a.offset)


def test_first_last_offset(hit_list, offsets):
    assert offsets[0] == hit_list.first_offset()
    assert offsets[-1] == hit_list.last_offset()
    assert (offsets[0], offsets[-1]) == hit_list.first_last_offset()


def test_empty_handling(hit_list):
    assert all(HitList([]).column == hit_list.between(500, 750).column)
    assert HitList([]).df.empty
    assert hit_list.between(500, 750).df.empty


def test_between(hit_list, hits, offsets):
    assert all(
        HitList(hits[0:1]) ==
        hit_list.between(offsets[0], offsets[1])
    )
    assert all(
        HitList(hits[0:1]) ==
        hit_list.between(offsets[0], offsets[1], include_ends=(True, False))
    )
    assert all(
        HitList(hits[0:2]) ==
        hit_list.between(offsets[0], offsets[1], include_ends=(True, True))
    )
    assert hit_list.between(
        offsets[0], offsets[1], include_ends=(False, False)
    ).df.empty

    assert (
        HitList(hits[1:2]).to_numpy() ==
        hit_list.between(offsets[0], offsets[1],include_ends=(False, True)).to_numpy()
    ).all()


def test_append_timed(hit_list, hits,columns):
    assert 5 == len(hit_list.append(hits[0]))


def test_append_timed_list(hit_list, hits, columns):
    assert 8 == len(hit_list.append(hit_list))


def test_append_series(hit_list, hits, columns):
    assert 5 == len(hit_list.append(hit_list[0].data))


def test_append_df(hit_list, columns):
    assert 8 == len(hit_list.append(hit_list.df))

import pandas as pd
import pytest

from reamber.base.lists import TimedList
from reamber.base.lists.notes.HitList import HitList


def test_type(timed_list):
    assert isinstance(timed_list.df, pd.DataFrame)


def test_offsets(timed_list, offsets):
    assert all(offsets == timed_list.offset.to_list())


def test_offsets_change(timed_list, offsets, randintp):
    timed_list.offset += randintp
    assert all(offsets + randintp == timed_list.offset.to_list())


def test_init_single_and_multiple(timeds):
    """ Check if 1-item list init == 1-item init """
    assert all(TimedList(timeds[:1]) == TimedList(timeds[0]))


def test_ix_slice(timed_list, timeds):
    sliced = timed_list[:2]
    assert isinstance(sliced, TimedList)
    assert 2 == len(sliced)
    assert all(HitList(timeds[:2]) == sliced)


def test_ix_bool(timed_list, offsets):
    sliced = timed_list[timed_list.offset < offsets[2]]
    assert 2 == len(sliced)
    assert all(offsets[:2] == sliced[:2].offset)


def test_loc(timed_list, randintp):
    timed_list.loc[0].offset += randintp
    timed_list.loc[0, 'offset'] += randintp
    assert randintp * 2 == timed_list.iloc[0].offset


def test_iloc(timed_list, randintp):
    timed_list.iloc[0] = randintp
    assert randintp == timed_list.iloc[0].offset


def test_first_last_offset(timed_list, offsets):
    assert offsets[0] == timed_list.first_offset()
    assert offsets[-1] == timed_list.last_offset()
    assert (offsets[0], offsets[-1]) == timed_list.first_last_offset()


def test_empty_handling(timed_list, offsets):
    assert all(TimedList([]).offset == timed_list.after(offsets[-1]).offset)
    assert TimedList([]).df.empty


@pytest.mark.parametrize(
    'include_ends,slc',
    [
        [(True, False), slice(0, 1)],
        [(False, True), slice(1, 2)],
        [(True, True), slice(0, 2)],
        [(False, False), slice(0, 0)]
    ]
)
def test_between(timed_list, timeds, offsets, include_ends, slc):
    assert all(
        TimedList(timeds[slc]).to_numpy() ==
        timed_list.between(offsets[0], offsets[1],
                           include_ends=include_ends).to_numpy()
    )


def test_append_timed(timed_list, timeds):
    assert len(timed_list) + 1 == len(timed_list.append(timeds[0]))


def test_append_timed_list(timed_list):
    assert len(timed_list) * 2 == len(timed_list.append(timed_list))


def test_append_series(timed_list):
    assert len(timed_list) + 1 == len(timed_list.append(timed_list[0].data))


def test_append_df(timed_list):
    assert len(timed_list) * 2 == len(timed_list.append(timed_list.df))


def test_from_dict(timed_list, offsets):
    assert all(timed_list ==
               TimedList.from_dict([dict(offset=o) for o in offsets]))
    assert all(timed_list ==
               TimedList.from_dict(dict(offset=offsets)))

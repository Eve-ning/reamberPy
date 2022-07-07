import pytest

from reamber.base.lists.notes.HitList import HitList


def test_in_columns(hit_list, offsets, columns):
    in_cols = hit_list.in_columns(columns[:2])
    assert 2 == len(in_cols)
    assert all(hit_list[:2] == in_cols)


def test_loose_append(hit_list, randintp):
    """ This tests if TimedList is able to append a Dictionary with missing
        variables, defaulting to the defaults
    """
    hit_list = hit_list.append(
        HitList.from_dict(
            {'offset': [randintp, -randintp]}
        )
    )
    assert hit_list.offset.tolist()[-2] == randintp
    assert hit_list.offset.tolist()[-1] == -randintp
    assert hit_list.column.tolist()[-2] == 0
    assert hit_list.column.tolist()[-1] == 0


def test_loose_append_bad(hit_list, randintp):
    with pytest.raises(ValueError):
        hit_list = hit_list.append(
            HitList.from_dict(
                {'bad_name': [randintp, -randintp]}
            )
        )

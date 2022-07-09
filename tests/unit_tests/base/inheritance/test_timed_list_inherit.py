import pytest

from reamber.base.Property import list_props
from reamber.base.lists import TimedList
from tests.unit_tests.base.inheritance.test_timed_inherit import TimedInherit


@list_props(TimedInherit)
class TimedListInherit(TimedList[TimedInherit]):
    ...


@pytest.fixture
def tl() -> TimedListInherit:
    return TimedListInherit([
        TimedInherit(offset=i, float_arg=i, int_arg=i, str_arg=f'{i}',
                     bool_arg=bool(i))
        for i in range(2)
    ])


def test_df_names(tl):
    assert tl.df.columns.to_list() == \
           ['offset', 'float_arg', 'int_arg', 'str_arg', 'bool_arg']


def test_prop_getter(tl):
    assert tl.float_arg.to_list() == [0, 1]
    assert tl.int_arg.to_list() == [0, 1]
    assert tl.str_arg.to_list() == ['0', '1']
    assert tl.bool_arg.to_list() == [False, True]


def test_prop_setter(tl):
    tl.float_arg = 0
    tl.int_arg = 0
    tl.str_arg = '0'
    tl.bool_arg = False
    assert tl.float_arg.to_list() == [0, 0]
    assert tl.int_arg.to_list() == [0, 0]
    assert tl.str_arg.to_list() == ['0', '0']
    assert tl.bool_arg.to_list() == [False, False]


def test_prop_defaults():
    defaults = TimedListInherit._default()
    assert all(defaults['float_arg'] == 1.0)
    assert all(defaults['int_arg'] == 1)
    assert all(defaults['str_arg'] == 'foo')
    assert all(defaults['bool_arg'])


def test_item_class():
    assert TimedListInherit._item_class() == TimedInherit

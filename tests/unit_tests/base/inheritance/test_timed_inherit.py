import pytest

from reamber.base import Timed, item_props



@item_props()
class TimedInherit(Timed):

    def __init__(self,
                 offset: float,
                 float_arg: float,
                 int_arg: int,
                 str_arg: str,
                 bool_arg: bool, **kwargs):
        super().__init__(
            offset=offset,
            float_arg=float_arg,
            int_arg=int_arg,
            str_arg=str_arg,
            bool_arg=bool_arg, **kwargs
        )

    _props = dict(
        float_arg=['float', 1.0],
        int_arg=['int', 1],
        str_arg=['str', 'foo'],
        bool_arg=['bool', True],
    )


@pytest.fixture
def timed_inherit(randintp):
    return TimedInherit(
        offset=randintp,
        float_arg=randintp,
        int_arg=randintp,
        str_arg=str(randintp),
        bool_arg=randintp % 2 == 0,
    )


def test_get_args(timed_inherit, randintp):
    assert timed_inherit.offset == randintp
    assert timed_inherit.float_arg == randintp
    assert timed_inherit.int_arg == randintp
    assert timed_inherit.str_arg == str(randintp)
    assert timed_inherit.bool_arg == (randintp % 2 == 0)

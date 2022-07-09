import pandas as pd
import pytest

from reamber.base import Series


class Subclass(Series):

    def __init__(self, arg1, arg2, **kwargs):
        super(Subclass, self).__init__(arg1=arg1, arg2=arg2, **kwargs)

    @staticmethod
    def _from_series_allowed_names():
        return ['arg1', 'arg2']


def test_from_series(rand):
    instance = Subclass.from_series(
        pd.Series(dict(arg1=rand, arg2=rand + 1, arg3=rand + 2))
    )
    assert instance.data['arg1'] == rand
    assert instance.data['arg2'] == rand + 1
    with pytest.raises(KeyError):
        _ = instance.data['arg3']


@pytest.mark.parametrize(
    'args',
    [{}, {'arg1': 0}, {'arg1': 0, 'arg3': 0}]
)
def test_from_series_bad_args(args):
    with pytest.raises(TypeError):
        Subclass.from_series(pd.Series(args, dtype=object))


def test_init(rand):
    instance = Subclass(arg1=rand, arg2=rand + 1)
    assert instance.data['arg1'] == rand
    assert instance.data['arg2'] == rand + 1


def test_deepcopy(rand):
    i = Subclass(arg1=rand, arg2=rand)
    assert i is not Subclass(arg1=rand, arg2=rand)
    assert i is not i.deepcopy()
    j = i
    assert i == j


def test_eq(rand):
    assert Subclass(arg1=rand, arg2=rand) == Subclass(arg1=rand, arg2=rand)

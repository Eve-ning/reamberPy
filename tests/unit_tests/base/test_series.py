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



def test_init(rand):
    instance = Subclass(arg1=rand, arg2=rand + 1)
    assert instance.data['arg1'] == rand
    assert instance.data['arg2'] == rand + 1

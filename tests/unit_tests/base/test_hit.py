import pandas as pd
import pytest

from reamber.base import Hit


@pytest.fixture
def hit():
    return Hit(offset=1000, column=1)


def test_type(hit):
    assert isinstance(hit.data, pd.Series)


def test_from_series(hit):
    assert Hit.from_series(pd.Series(dict(offset=1000, column=1))), hit

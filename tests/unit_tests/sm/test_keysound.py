import pandas as pd

from reamber.sm import SMKeySound
from tests.test.sm.test_fixture import sm_mapset


# def test_type(sm_mapset):
#     assert isinstance(sm_mapset[0].keysounds[0], SMKeySound)

def test_from_series():
    keysound = SMKeySound.from_series(pd.Series(dict(offset=1000, column=1)))
    assert SMKeySound(1000, 1) == keysound

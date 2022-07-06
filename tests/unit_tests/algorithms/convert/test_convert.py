from typing import Iterable

import pytest

from reamber.algorithms.convert import *


@pytest.mark.parametrize(
    'converters,map',
    [([BMSToOsu, BMSToSM, BMSToQua], 'bms_map'),
     ([OsuToBMS, OsuToQua, OsuToSM], 'osu_map'),
     ([SMToBMS, SMToOsu, SMToQua], 'sm_mapset'),
     ([O2JToBMS, O2JToOsu, O2JToQua, O2JToSM], 'o2j_mapset'), ]
)
def test_conversions(converters, map, request):
    for converter in converters:
        convert = converter().convert(request.getfixturevalue(map))
        if isinstance(convert, Iterable):
            convert[0].write()
        else:
            convert.write()

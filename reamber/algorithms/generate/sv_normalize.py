from __future__ import annotations

from typing import overload

from reamber.osu import OsuMap
from reamber.osu.lists import OsuSvList
from reamber.quaver import QuaMap
from reamber.quaver.lists import QuaSvList


@overload
def sv_normalize(m: OsuMap) -> OsuSvList: ...


@overload
def sv_normalize(m: QuaMap) -> QuaSvList: ...


def sv_normalize(m: OsuMap | QuaMap) -> OsuSvList | QuaSvList:
    """ Normalizes a map with respect to its dominant BPM.

    Args:
        m: An instance of a OsuMap or QuaMap

    Examples:
        Normalize an OsuMap::

            >>> osu = OsuMap.read_file(...)
            >>> osu_sv_norm = sv_normalize(osu)
            >>> osu.svs = osu.svs.append(osu_sv_norm)

    Returns:
        An OsuSvList or QuaSvList, depending on the input type
    """
    return ...


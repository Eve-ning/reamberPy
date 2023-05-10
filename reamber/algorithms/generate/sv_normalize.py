from __future__ import annotations

from typing import overload

from reamber.algorithms.utils import dominant_bpm
from reamber.osu import OsuMap
from reamber.osu.lists import OsuSvList
from reamber.quaver import QuaMap
from reamber.quaver.lists import QuaSvList


@overload
def sv_normalize(m: OsuMap, override_bpm: float = None) -> OsuSvList: ...


@overload
def sv_normalize(m: QuaMap, override_bpm: float = None) -> QuaSvList: ...


def sv_normalize(m: OsuMap | QuaMap, override_bpm: float = None) -> OsuSvList | QuaSvList:
    """ Normalizes a map with respect to its dominant BPM.

    The new SVs returned will inherit attributes of the respective BPMs normalized.

    Notes:
        This will only return the necessary SVs to append to the map.
        It may be good to have additional logic to handle overlapping SVs, if any.

    Args:
        m: An instance of a OsuMap or QuaMap
        override_bpm: If not None, use this instead of using the dominant calculated bpm.

    Examples:
        Normalize an OsuMap::

            >>> osu = OsuMap.read_file(...)
            >>> osu_sv_norm = sv_normalize(osu)
            >>> osu.svs = osu.svs.append(osu_sv_norm)

            You may need to remove duplicates if there are SVs already present

            >>> osu.svs = OsuSvList(osu.svs.df.drop_duplicates())

    Returns:
        An OsuSvList or QuaSvList, depending on the input type
    """

    # Get the dominant BPM
    bpm_dom = override_bpm if override_bpm else dominant_bpm(m)

    # Retrieve the bpm DataFrame to find the relative normalization necessary
    df_bpm = m.bpms.df

    # Calculate multiplier necessary
    df_bpm['multiplier'] = bpm_dom / df_bpm['bpm']

    # Filter out sv columns via the names and create out SVList
    SvList = m.svs.__class__

    return SvList(df_bpm.loc[:, SvList([]).df.columns])

""" Can't find a better name for this without it being too vague or generic """

from typing import overload

from reamber.osu.OsuMapObj import OsuMapObj, MapObj
from reamber.sm.SMMapSetObj import SMMapSetObj
from reamber.quaver.QuaMapObj import QuaMapObj

from copy import deepcopy
from reamber.algorithms.analysis.playField.PlayField import PlayField


def ss(self, pf: PlayField) -> PlayField:
    return PlayField(self)


@overload
def rate(m: OsuMapObj, by: float, inplace: bool = False) -> OsuMapObj: ...
@overload
def rate(m: QuaMapObj, by: float, inplace: bool = False) -> QuaMapObj: ...
@overload
def rate(s: SMMapSetObj, by: float, inplace: bool = False) -> SMMapSetObj: ...
def rate(m: MapObj, by: float, inplace: bool = False) -> MapObj:
    """ Speeds up the map by rate specified.

    :param m: The map
    :param by: The by, 0.8 means 80% speed, 1.2 means 120% speed
    :param inplace: If True, modifies the map in place without returning
    """
    assert 0 < by, "by cannot be negative or zero"

    m_ = m if inplace else deepcopy(m)

    if isinstance(m_, OsuMapObj):
        for bpm in m_.bpms:
            bpm.offset /= by
            bpm.bpm *= by
        for sv in m_.svs:
            sv.offset /= by
        for hit in m_.notes.hits():
            hit.offset /= by
        for hold in m_.notes.holds():
            hold.offset /= by
            hold.length /= by
        for samp in m_.samples:
            samp.offset /= by
        m_.previewTime /= by
        # TODO: Implement rating up of storyboard if implemented

    elif isinstance(m_, QuaMapObj):
        for bpm in m_.bpms:
            bpm.offset /= by
            bpm.bpm /= by
        for sv in m_.svs:
            sv.offset /= by
        for hit in m_.notes.hits():
            hit.offset /= by
        for hold in m_.notes.holds():
            hold.offset /= by
            hold.length /= by
        m_.songPreviewTime /= by

    elif isinstance(m_, SMMapSetObj):
        for map in m_.maps:
            for bpm in map.bpms:
                bpm.offset *= by
                bpm.bpm /= by
        m_.sampleStart /= by
        m_.sampleLength /= by

    return None if inplace else m_

""" Can't find a better name for this without it being too vague or generic """

from typing import overload

from reamber.osu.OsuMapObj import OsuMapObj, MapObj
from reamber.sm.SMMapSetObj import SMMapSetObj
from reamber.quaver.QuaMapObj import QuaMapObj

from copy import deepcopy


@overload
def rate(m: OsuMapObj, rate: float, inplace: bool = False) -> MapObj: ...
@overload
def rate(m: QuaMapObj, rate: float, inplace: bool = False) -> MapObj: ...
@overload
def rate(s: SMMapSetObj, rate: float, inplace: bool = False) -> MapObj: ...
def rate(m: MapObj, rate: float, inplace: bool = False) -> MapObj:
    """ Speeds up the map by rate.

    :param m: The map
    :param rate: The rate, 0.8 means 80% speed, 1.2 means 120% speed
    :param inplace: If True, modifies the map in place without returning
    """
    assert 0 < rate, "Rate cannot be negative or zero"

    m_ = m if inplace else deepcopy(m)

    if isinstance(m_, OsuMapObj):
        for bpm in m_.bpms:
            bpm.offset /= rate
            bpm.bpm *= rate
        for sv in m_.svs:
            sv.offset /= rate
        for hit in m_.notes.hits():
            hit.offset /= rate
        for hold in m_.notes.holds():
            hold.offset /= rate
            hold.length /= rate
        for samp in m_.samples:
            samp.offset /= rate
        m_.previewTime /= rate
        # TODO: Implement rating up of storyboard if implemented

    elif isinstance(m_, QuaMapObj):
        for bpm in m_.bpms:
            bpm.offset /= rate
            bpm.bpm /= rate
        for sv in m_.svs:
            sv.offset /= rate
        for hit in m_.notes.hits():
            hit.offset /= rate
        for hold in m_.notes.holds():
            hold.offset /= rate
            hold.length /= rate
        m_.songPreviewTime /= rate

    elif isinstance(m_, SMMapSetObj):
        for map in m_.maps:
            for bpm in map.bpms:
                bpm.offset *= rate
                bpm.bpm /= rate
        m_.sampleStart /= rate
        m_.sampleLength /= rate

    return None if inplace else m_

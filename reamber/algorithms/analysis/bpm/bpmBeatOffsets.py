""" This algorithm finds the offsets for every 1/1 (4th) beat in the maps' bpm list

To support image/image algorithm
"""

from reamber.base.lists.BpmList import BpmList
from reamber.base.RAConst import RAConst
from reamber.osu.lists.OsuBpmList import OsuBpmList
from typing import overload, List


def bpmBeatOffsets(bpms: OsuBpmList, nths: float = 1.0,
                   lastOffset: float = None):  # to convert into BPMList later
    """ Gets all of the nth snap offsets

    :param bpms: The map's bpm
    :param nths: Specifies the beat's snap, 1 = "1st"s, 4 = "4th"s, 16 = "16th"s
    :param lastOffset: The last offset to consider, if None, it uses the last BPM
    """
    offsets: List[float] = []
    bpms_ = bpms.sorted().data()

    currBpmI   = 0
    currOffset = bpms_[currBpmI].offset
    currBpm    = bpms_[currBpmI]
    snapLength = RAConst.minToMSec(1 / nths / currBpm.bpm)
    if lastOffset is None: lastOffset = bpms_[-1].offset

    nextBpm = None if currBpmI + 1 == len(bpms_) else bpms_[currBpmI + 1]

    while currOffset <= lastOffset:
        offsets.append(currOffset)
        currOffset += snapLength
        if nextBpm and currOffset > nextBpm.offset:
            currBpm = nextBpm
            currOffset = nextBpm.offset
            snapLength = RAConst.minToMSec(1 / nths / currBpm.bpm)
            currBpmI += 1
            nextBpm = None if currBpmI + 1 == len(bpms_) else bpms_[currBpmI + 1]
            continue

    return offsets

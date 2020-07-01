from typing import List
from reamber.base.Bpm import Bpm
from reamber.base.lists.TimedList import TimedList
from reamber.base.RAConst import RAConst
from abc import ABC


class BpmList(List[Bpm], TimedList, ABC):
    """ A List that holds a list of Bpms, useful to do group Bpm operations """

    def data(self) -> List[Bpm]:
        """ Grabs the list of Bpm """
        return self

    def bpms(self) -> List[float]:
        """ Grabs a list of Bpm values only """
        return self.attribute('bpm')

    def snapOffsets(self, nths: float = 1.0,
                    lastOffset: float = None) -> List[float]:
        """ Gets all of the nth snap offsets

        For example::

            SEC     1   2   3   4   5   6   7   8   9   10  11  12  13  14  ...
            BPM     15                          7.5                         ...
            SNAP    4/4 1/4 2/4 3/4 4/4 1/4 2/4 4/4 1/8 2/8 3/8 4/8 5/8 6/8 ...
            BEAT    1               2           3
            nths=1  ^               ^           ^
            nths=2  ^       ^       ^       ^   ^               ^
            nths=4  ^   ^   ^   ^   ^   ^   ^   ^       ^       ^       ^
            nths=8  ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^   ^   ^   ^   ^   ^   ^

        * Note: 15 BPM = 1 Beat per 4 seconds, 7.5 = 1 Beat per 8 seconds

        The `^` indicates what offsets will be returned.

        :param nths: Specifies the beat's snap, 1 = "1st"s, 4 = "4th"s, 16 = "16th"s
        :param lastOffset: The last offset to consider, if None, it uses the last BPM
        """
        offsets: List[float] = []
        bpms_ = self.sorted().data()

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

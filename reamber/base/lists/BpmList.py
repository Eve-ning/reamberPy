from abc import ABC
from typing import List

from reamber.base.Bpm import Bpm
from reamber.base.RAConst import RAConst
from reamber.base.lists.TimedList import TimedList


class BpmList(List[Bpm], TimedList, ABC):
    """ A List that holds a list of Bpms, useful to do group Bpm operations """

    def data(self) -> List[Bpm]:
        """ Grabs the list of Bpm """
        return self

    def bpms(self) -> List[float]:
        """ Grabs a list of Bpm values only """
        return self.attribute('bpm')

    def snap_offsets(self, nths: float = 1.0,
                     last_offset: float = None) -> List[float]:
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
        :param last_offset: The last offset to consider, if None, it uses the last BPM
        """
        offsets: List[float] = []
        bpms_ = self.sorted().data()

        curr_bpm_i  = 0
        curr_offset = bpms_[curr_bpm_i].offset
        curr_bpm    = bpms_[curr_bpm_i]
        snap_length = RAConst.min_to_msec(1 / nths / curr_bpm.bpm)
        if last_offset is None: last_offset = bpms_[-1].offset

        next_bpm = None if curr_bpm_i + 1 == len(bpms_) else bpms_[curr_bpm_i + 1]

        while curr_offset <= last_offset:
            offsets.append(curr_offset)
            curr_offset += snap_length
            if next_bpm and curr_offset > next_bpm.offset:
                curr_bpm = next_bpm
                curr_offset = next_bpm.offset
                snap_length = RAConst.min_to_msec(1 / nths / curr_bpm.bpm)
                curr_bpm_i += 1
                next_bpm = None if curr_bpm_i + 1 == len(bpms_) else bpms_[curr_bpm_i + 1]
                continue

        return offsets

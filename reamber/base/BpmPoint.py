from __future__ import annotations

from reamber.base.TimedObject import TimedObject as TimedObject
from reamber.base.RAConst import RAConst
from dataclasses import dataclass

from typing import List
from typing import Tuple
from typing import Union


@dataclass
class BpmPoint(TimedObject):
    bpm: float = 120.0
    metronome: int = 4

    def beatLength(self) -> float:
        return RAConst.minToMSec(1.0 / self.bpm)

    def metronomeLength(self) -> float:
        return self.beatLength() * self.metronome

    def beat(self, tps: List[BpmPoint]):
        """
        :type tps: This should be a list of TimingPoints that this resides in
        """
        return BpmPoint.getBeats([self.offset], tps)[0]

    # Beats are used for the StepMania format
    # One large caveat for beats is that it requires looping through the BPM Points of the map to
    # calculate 1 single beat
    # Hence There is a getBeats and getBeat, where if getBeats is used for a list instead of looping through
    # getBeat, it'll be marginally faster.

    @staticmethod
    def getBeats(offsets: Union[List[float], List[TimedObject], float],
                 bpms: List[BpmPoint]) -> List[float]:
        """
        Gets the beat numbers from offsets provided, this is relative to the first Timing Point
        :param offsets: Offsets to find beat from, can be a list of TOs or floats or a single float
        :param bpms: The Global BPM list
        :return: Beat numbers with respect to the first Timing Point provided.
        """
        # The idea here is to loop through the BPM Points once while filling the beats list with the correct offsets
        # 1.  For each offset:
        # 1.1 Go through the bpms until we find the 2 BPMs that sandwich it
        #     [BPM] [Offset] [BPM]
        # 1.2 If the offset cannot be sandwiched, then we use the last bpm to reference
        #     [BPM] [Offset]
        #
        # 2.  While we are looping through BPMs to find, we need to take note of the prior Beat
        # 2.1 For each BPM iteration, we update bpmPrevBeat
        #
        # 3.  Once we found the sandwich, we find the difference in offsets and find out the beat of the offset

        # Main problem obviously is if the offsets or bpms are not sorted, it'll break the algorithm
        # So we need to get a sorted offset and sorted bpm
        # Unfortunately, unless we force implement sorting on the higher level,
        # this sorting algorithm will have to stay

        # Firstly, coerce the offsets into a List[float] if it's not already
        offsets_ = offsets if isinstance(offsets, List) else [offsets]
        offsets_: Union[List[TimedObject], List[float]]
        if len(offsets_) == 0: return []
        offsets_ = [x.offset for x in offsets_] if isinstance(offsets_[0], TimedObject) else offsets_
        offsets_: List[float]

        # We attach an enum to the original list and sort by the offsets, this sorts it once
        offsetsSorted_: List[Tuple[int, float]] = [x for x in sorted(enumerate(offsets_), key=lambda x:x[1])]
        offsetsSortedOrder: List[int]  # This is the original order
        offsetsSorted: List[float]
        offsetsSortedOrder, offsetsSorted = zip(*offsetsSorted_)  # Unpacks into the original order and sort

        del offsetsSorted_, offsets_

        bpmIndex = 0
        bpmPrevBeat = 0  # If we skip TPs, we have to account for their previous beat

        beats: List[float] = []

        for offset in offsetsSorted:
            # Shift TP such that tp is the latest
            while bpmIndex != len(bpms) - 1 and \
                    not (bpms[bpmIndex].offset <= offset < bpms[bpmIndex + 1].offset):
                bpmIndex += 1
                bpmPrevBeat += (bpms[bpmIndex].offset - bpms[bpmIndex - 1].offset) /\
                                bpms[bpmIndex - 1].beatLength()

            beats.append(bpmPrevBeat + ((offset - bpms[bpmIndex].offset) / bpms[bpmIndex].beatLength()))

        # Sorts beats by original order
        return [x for x, _ in sorted(zip(beats, offsetsSortedOrder), key=lambda x:x[1])]

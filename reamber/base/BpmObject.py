from __future__ import annotations

from reamber.base.TimedObject import TimedObject as TimedObject
from reamber.base.RAConst import RAConst
from dataclasses import dataclass

from typing import List
from typing import Tuple
from typing import Union


@dataclass
class BpmObject(TimedObject):
    bpm: float = 120.0
    metronome: int = 4

    def beatLength(self) -> float:
        """ Returns the length of the beat in ms """
        return RAConst.minToMSec(1.0 / self.bpm)

    def metronomeLength(self) -> float:
        """ Returns the length of the beat in metronome """
        return self.beatLength() * self.metronome

    def beat(self, bpms: List[BpmObject]):
        """ Gets the beat of the current BPM Point w.r.t. bpms """
        return BpmObject.getBeats([self.offset], bpms)[0]

    # Beats are used for the StepMania format
    # One large caveat for beats is that it requires looping through the BPM Points of the map to
    # calculate 1 single beat
    # Hence There is a getBeats and getBeat, where if getBeats is used for a list instead of looping through
    # getBeat, it'll be marginally faster.

    @staticmethod
    def getBeats(offsets: Union[List[float], List[TimedObject], float],
                 bpms: List[BpmObject]) -> List[float]:
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
        # noinspection PyTypeChecker
        offsetsSorted_: List[Tuple[int, float]] = [x for x in sorted(enumerate(offsets_), key=lambda x:x[1])]
        offsetsSortedOrder: List[int]  # This is the original order
        offsetsSorted: List[float]
        offsetsSortedOrder, offsetsSorted = zip(*offsetsSorted_)  # Unpacks into the original order and sort

        del offsetsSorted_, offsets_

        bpmIndex = 0
        bpmPrevBeat = 0  # If we skip TPs, we have to account for their previous beat

        beats: List[float] = []
        bpms.sort(key=lambda x: x.offset)

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

    @staticmethod
    def alignBpms(bpms: List[BpmObject],
                  BEAT_ERROR_THRESHOLD: float = 0.001,
                  BEAT_CORRECTION_FACTOR: float = 5.0) -> List[BpmObject]:
        """
        Ensures that all BPMs are on an integer measure by adding or amending
        :param bpms: The BPMs
        :param BEAT_ERROR_THRESHOLD: If the fraction change in beat's is more than this, we append a new BPM, else we
        create a new bpm. i.e. if there's too many high BPM points, then increase this
        :param BEAT_CORRECTION_FACTOR: The number of beats to search prior to the affected beat to amend. i.e. if
        there are too many incorrectly snapped notes DUE TO ADDED BPMs then decrease this
        :return: The new and old BPMs
        """
        # Summary
        # We ensure that all BPMs are on an integer measure, this makes it such that it's easier to snap

        # This will be a conditional of alignBpms
        # If the BPM is misaligned to a measure
        #   If there is a BPM less than or equal to a beat prior
        #       Adjust that one
        #   Else
        #       Create a BPM 1 Beat prior

        # Edge cases
        # Sometimes the beat is like X.000001
        # For this, we wouldn't want to add a BPM at X and shift this to X+1
        # This is because we'll get a very high BPM here and it'll look ugly
        # For this, we will add a BPM at X-1 or amend X-1.

        # Hence
        # If X.000        : Don't change anything
        # If Amend        : Just amend the previous
        # If X.000 ~ X.001: Change X-1
        # If X.001 ~ X.999: Change X   & Move to X + 1
        # BEAT_ERROR_THRESHOLD

        # The beat correction factor defines how many beats to look behind to correct a bpm point
        # BEAT_CORRECTION_FACTOR

        bpmBeats = BpmObject.getBeats(bpms, bpms)
        bpmsNew: List[BpmObject] = [bpms[0]]
        for bpmIndex in range(1, len(bpms)):  # Note We don't touch the first bpm, that's assumed to be 0.0
            bpmPrev = bpms[bpmIndex - 1]
            bpmCurr = bpms[bpmIndex]
            bpmBeatPrev = bpmBeats[bpmIndex - 1]
            bpmBeatCurr = bpmBeats[bpmIndex]

            bpmBeatError = (bpmBeatCurr - bpmBeatPrev) % 1.0

            if bpmBeatError == 0.0:
                pass
            elif bpmCurr.offset - bpmCurr.beatLength() * BEAT_CORRECTION_FACTOR <= bpmPrev.offset <= bpmCurr.offset:
                # This is the case when the previous BPM is within (1 * BCF) beats of the current BPM
                # Instead of inserting another BPM, we amend the previous BPM
                bpmsNew[-1].bpm = 1 / RAConst.mSecToMin(bpmCurr.offset - bpmPrev.offset)
            elif bpmBeatError < BEAT_ERROR_THRESHOLD:
                # As defined, if we happen to have an error that's less than the threshold, instead of forcing
                # a new bpm, we amend the prior bpm OR add a bpm point 1 beat before
                bpmsNew.append(BpmObject(offset=bpmCurr.offset - (1.0 + bpmBeatError) * bpmPrev.beatLength(),
                                         bpm=1.0 / RAConst.mSecToMin(bpmPrev.beatLength() * (1 + bpmBeatError))))
            else:
                # This is the case when the beat is significant enough that it warrants a BPM point in its place
                bpmsNew.append(BpmObject(offset=bpmCurr.offset - bpmBeatError * bpmPrev.beatLength(),
                                         bpm=1.0 / RAConst.mSecToMin(bpmPrev.beatLength() * bpmBeatError)))

            bpmsNew.append(bpmCurr)

        return bpmsNew

    # This is the previous method to alignBpms, it's not very good haha...
    # @staticmethod
    # def alignBpms(bpmPoints: List[BpmObject]) -> List[BpmObject]:
    #     # The naive approach is to forcibly link all bpmBeats together
    #     # We do this by creating a BPM 1ms before all incorrectly offset BPMs and push that BPM forward to an integer
    #     # E.g.
    #     # [1, 2.5, 3.5, 5] -> [1, 2.5 - e, 3, 4.5, 6] -> [1, 2.5 - e, 3, 4.5 - e, 5, 7]
    #     # where e is the beat snap for 1 ms, it'll be based on the previous BPM
    #
    #     # Formula
    #     # BPM: 60000 - mod * 60000 + prevBPM
    #     # Offset: currBpm.offset - prevBpm/60000
    #
    #     bpmPointsSorted = sorted(bpmPoints, key=lambda x: x.offset)
    #     bpmBeats = BpmObject.getBeats(bpmPointsSorted, bpmPointsSorted)
    #     newBpms: List[BpmObject] = [bpmPointsSorted[0]]
    #
    #     # We naively assume that all bpms are incorrect except the first
    #     for bpmIndex, (bpm, bpmBeat) in enumerate(zip(bpmPointsSorted[1:], bpmBeats[1:])):
    #         beatShift: float = bpmBeat % 1.0
    #
    #         # This means that if the measure reset is within 1/4, 16th of a beat, and has an error of < 0.001, we
    #         # will adjust it, else ignore
    #         if beatShift % 0.125 < 0.001 or beatShift % 0.125 > 0.124:
    #             newBpms.append(bpm)
    #             continue
    #
    #         beatShift = beatShift if 0.0 < beatShift <= 1.0 else 1.0
    #
    #         # # Correction BPM (4th) < Refer to 16ths >
    #         # # This would be a large change in BPM
    #         # newBpms.append(BpmObject(
    #         #     # This will shift the offset to the closest prev integer beat
    #         #     offset=bpm.offset - beatShift * bpmPoints[bpmIndex].beatLength(),
    #         #     bpm=1 / RAConst.mSecToMin(bpmPoints[bpmIndex].beatLength() * beatShift)))
    #
    #         # Correction BPM (16th)
    #         # The idea here would be a bit different, we'll have the correction and shifted BPM on integers.
    #         # Let's say we have the beatShift as 0.333
    #         # Then we adjust the Correction to 0.0, the Shift to 1.0, we'll then calculate the required BPM
    #         # Side-effect would be that notes may have problems syncing to the new BPM, we'll deal with that
    #         # later
    #         newBpms.append(BpmObject(
    #             # This will shift the offset to the closest prev integer beat
    #             offset=bpm.offset - beatShift * bpmPoints[bpmIndex].beatLength(),
    #             bpm=1 / RAConst.mSecToMin(bpmPoints[bpmIndex].beatLength() * beatShift)))
    #
    #         # Correction BPM (192nd)
    #         # newBpms.append(BpmObject(offset=bpm.offset - bpmPoints[bpmIndex].beatLength() / 48,  # 1/192
    #         #                         bpm=(1 - beatOffset + 1 / 48) /
    #         #                             (RAConst.mSecToMin(bpmPoints[bpmIndex].beatLength()) / 48)))
    #
    #         # Correction BPM (1ms)
    #         # newBpms.append(BpmObject(offset=bpm.offset - 1,
    #         #                         bpm=60000 - beatShift * 60000 + bpmPoints[bpmIndex].bpm))
    #
    #         # Shifted BPM
    #         newBpms.append(bpm)
    #
    #     # This removes all repeating offsets, priority goes to the new BPMs
    #     bpmIndexToRemove = []
    #     for bpmIndex in range(len(newBpms) - 1):
    #         if newBpms[bpmIndex + 1].offset == newBpms[bpmIndex].offset:
    #             bpmIndexToRemove.append(bpmIndex)
    #
    #     bpmIndexToRemove.reverse()
    #     for bpmIndex in bpmIndexToRemove:
    #         newBpms.pop(bpmIndex)
    #
    #     return newBpms

from __future__ import annotations

from reamber.base.TimedObject import TimedObject as TimedObject
from reamber.base.RAConst import RAConst
from dataclasses import dataclass

from typing import List


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
        return BpmPoint.getBeatFromOffset(self.offset, tps)

    @staticmethod
    def getBeatFromOffset(offset: float, tps: List[BpmPoint]) -> float:
        """
        Gets the beat number from offset provided, this is relative to the first Timing Point
        :param offset: Offset to find beat from
        :param tps: The Global TimingPoint list
        :return: Beat number with respect to the first Timing Point provided.
        """
        currBeat = 0
        tp = tps[0]
        if len(tps) > 1:
            for nextTp in tps[1:]:  # Searches through all next TPs to see if they are on the right or left
                if offset > nextTp.offset:
                    currBeat += (nextTp.offset - tp.offset) / tp.beatLength()
                    tp = nextTp
                else: break

        # Final LEFT TP is retained in the for loop
        currBeat += (offset - tp.offset) / tp.beatLength()
        return currBeat

    @staticmethod
    def getBeatsFromOffsets(offsets: List[float], tps: List[BpmPoint]) -> List[float]:
        """
        Gets the beat numbers from offsets provided, this is relative to the first Timing Point
        :param offsets: Offsets to find beat from
        :param tps: The Global TimingPoint list
        :return: Beat numbers with respect to the first Timing Point provided.
        """
        # TODO: Optimize this, this loops through the TPs multiple times
        return [BpmPoint.getBeatFromOffset(offset, tps) for offset in offsets]

    @staticmethod
    def getBeatFromTO(fromTO: TimedObject, tps: List[BpmPoint]) -> float:
        """
        Gets the beat number from offset provided, this is relative to the first Timing Point
        :param fromTO: Timing Point Offset to find beat from
        :param tps: The Global TimingPoint list
        :return: Beat number with respect to the first Timing Point provided.
        """
        return BpmPoint.getBeatFromOffset(fromTO.offset, tps)

    @staticmethod
    def getBeatsFromTOs(fromTOs: List[TimedObject], tps: List[BpmPoint]) -> List[float]:
        """
        Gets the beat numbers from offsets provided, this is relative to the first Timing Point
        :param fromTOs: Timing Point Offsets to find beat from
        :param tps: The Global TimingPoint list
        :return: Beat numbers with respect to the first Timing Point provided.
        """
        return BpmPoint.getBeatsFromOffsets([to.offset for to in fromTOs], tps)


from __future__ import annotations

import logging
import struct
from collections import deque
from dataclasses import dataclass, field
from typing import List, Union, Dict

from reamber.base.RAConst import RAConst
from reamber.o2jam.O2JBpmPoint import O2JBpmPoint
from reamber.o2jam.O2JHitObject import O2JHitObject
from reamber.o2jam.O2JHoldObject import O2JHoldObject

log = logging.getLogger(__name__)


class O2JNoteChannel:
    MEASURE_FRACTION: int = 0
    BPM_CHANGE      : int = 1
    COL_1           : int = 2
    COL_2           : int = 3
    COL_3           : int = 4
    COL_4           : int = 5
    COL_5           : int = 6
    COL_6           : int = 7
    COL_7           : int = 8
    COL_RANGE       : range = range(2, 9)
    AUTOPLAY_1      : int = 9
    AUTOPLAY_2      : int = 10
    AUTOPLAY_3      : int = 11
    AUTOPLAY_4      : int = 12
    AUTOPLAY_5      : int = 13
    AUTOPLAY_6      : int = 14
    AUTOPLAY_7      : int = 15
    AUTOPLAY_8      : int = 16
    AUTOPLAY_9      : int = 17
    AUTOPLAY_10     : int = 18
    AUTOPLAY_11     : int = 19
    AUTOPLAY_12     : int = 20
    AUTOPLAY_13     : int = 21
    AUTOPLAY_14     : int = 22
    AUTOPLAY_RANGE  : range = range(9,23)
    # Is there more?
    # Don't worry about the size of this obj, all of them are static.


@dataclass
class O2JEventMeasureChange:
    # When the channel is 0(fractional measure), the 4 bytes are a float,
    # indicating how much of the measure is actually used,
    # so if the value is 0.75, the size of this measure will be only 75% of a normal measure.
    fracLength: float = 1.0


@dataclass
class O2JEventPackage:
    measure: int = 0  # Len 4 (Int)
    channel: int = -1  # Len 2 (Short)
    # There's a Len 2 (Short) indicating how many events there are.
    # Then it's followed by that amount of events.
    events: List[Union[O2JBpmPoint, O2JHitObject, O2JHoldObject, O2JEventMeasureChange]] =\
        field(default_factory=lambda: [])

    @dataclass
    class O2JNote:
        # The purpose of this class is to facilitate conversion from measures into offset
        column: int = 0
        measure: float = 0.0  # Note that this measure is relative to the previous BPM

    @dataclass
    class O2JHold:
        column: int = 0
        measure: float = 0.0
        measureEnd: float = 0.0

    @staticmethod
    def readEventPackages(data: bytes, initBpm: float) -> List[O2JEventPackage]:
        """ Reads all events, this data found after the metadata (300:)
        :param initBpm: The very first bpm to use on beat 0
        :param data: All the event data in bytes.
        """
        packages: List[O2JEventPackage] = []
        dataQ = deque(data)

        # Column, Offset
        holdBuffer: Dict[int, O2JHoldObject] = {}

        # These parameters are used to track the notes' measures
        currBpm     = initBpm
        currMeasure = 0.0
        currOffset  = 0.0

        while True:
            if len(dataQ) == 0: break
            package = O2JEventPackage()
            packageData = []
            for i in range(8): packageData.append(dataQ.popleft())

            package.measure = struct.unpack("<i", bytes(packageData[0:4]))[0]
            package.channel = struct.unpack("<h", bytes(packageData[4:6]))[0]
            eventCount      = struct.unpack("<h", bytes(packageData[6:8]))[0]

            eventsData = []
            for i in range(4 * eventCount): eventsData.append(dataQ.popleft())
            eventsData = bytes(eventsData)
            if package.channel in O2JNoteChannel.COL_RANGE:
                package.events = O2JEventPackage.readEventsNote(eventsData, package.channel - 2, holdBuffer,
                                                                package.measure, currBpm, currOffset)
                currMeasure += 1
            elif package.channel == O2JNoteChannel.BPM_CHANGE:
                currBpm = O2JEventPackage.readEventsBpm(eventsData)
                # currMeasure = 0
                currOffset = RAConst.minToMSec(1 / currMeasure * 4 * currBpm)
                package.events.append(O2JBpmPoint(0, currBpm))
            elif package.channel == O2JNoteChannel.MEASURE_FRACTION:
                measureFrac = O2JEventPackage.readEventsMeasure(eventsData)
                # currMeasure += measureFrac
                package.events.append(O2JEventMeasureChange(measureFrac))
            else:
                pass
            packages.append(package)
        return packages

    @staticmethod
    def readEventsMeasure(eventsData: bytes) -> float:
        return struct.unpack("<f", eventsData[0:4])[0]

    @staticmethod
    def readEventsBpm(eventsData: bytes) -> float:
        return struct.unpack("<f", eventsData[0:4])[0]

    @staticmethod
    def readEventsNote(eventsData: bytes, column: int, holdBuffer: Dict[int, O2JHoldObject],
                       currMeasure: float, currBpm: float, currOffset: float) ->\
            List[Union[O2JHitObject, O2JHoldObject]]:
        notes = []

        eventCount = int(len(eventsData) / 4)

        log.debug(eventsData)
        for i in range(eventCount):
            enabled  = struct.unpack("<h", eventsData[0 + i * 4:2 + i * 4])[0]
            if enabled == 0: continue
            offset   = currOffset + RAConst.minToMSec((i / eventCount + currMeasure) * 4 / currBpm)
            volume   = struct.unpack("<s", eventsData[2 + i * 4:3 + i * 4])[0]
            pan      = struct.unpack("<s", eventsData[2 + i * 4:3 + i * 4])[0]
            noteType = struct.unpack("<s", eventsData[3 + i * 4:4 + i * 4])[0]
            log.debug(f"{column} @ {offset}")

            if noteType == O2JHitObject.INT:
                notes.append(O2JHitObject(volume=volume, pan=pan, offset=offset, column=column))
                log.debug(f"Appended Note {column} at {offset} ms")
            elif noteType == O2JHoldObject.INT_HEAD:
                holdBuffer[column] = O2JHoldObject(volume=volume, pan=pan, offset=offset, column=column, length=-1)
            elif noteType == O2JHoldObject.INT_TAIL:
                hold = holdBuffer.pop(column)
                hold.length = offset - hold.offset
                log.debug(f"Appended LNote {column} at {hold.offset} ms")
            else:
                pass
        pass




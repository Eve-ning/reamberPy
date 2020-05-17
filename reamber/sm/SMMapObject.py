from __future__ import annotations

from reamber.base.MapObject import MapObject
from reamber.base.BpmPoint import BpmPoint
from reamber.sm.SMMapObjectMeta import SMMapObjectMeta, SMMapObjectChartTypes
from reamber.sm.SMBpmPoint import SMBpmPoint
from reamber.sm.SMStop import SMStop
from reamber.sm.SMHitObject import SMHitObject
from reamber.sm.SMHoldObject import SMHoldObject
from reamber.sm.SMRollObject import SMRollObject
from reamber.sm.SMMineObject import SMMineObject
from reamber.sm.SMFakeObject import SMFakeObject
from reamber.sm.SMLiftObject import SMLiftObject
from reamber.sm.SMKeySoundObject import SMKeySoundObject

from dataclasses import dataclass
from typing import List
from typing import Dict

from numpy import gcd

import logging
log = logging.getLogger(__name__)


@dataclass
class SMMapObject(MapObject, SMMapObjectMeta):

    _SNAP_ERROR_BUFFER = 0.001

    @staticmethod
    def readString(map: str, bpms: List[SMBpmPoint], stops: List[SMStop]) -> SMMapObject:
        spl = map.split(":")
        map = SMMapObject()
        map._readNoteMetadata(spl[1:6])  # These contain the metadata

        # Splits measures by \n and filters out blank + comment entries
        measures: List[List[str]] =\
            [[snap for snap in measure.split("\n")
              if "//" not in snap and len(snap) > 0] for measure in spl[-1].split(",")]

        map._readNotes(measures, bpms=bpms, stops=stops)
        return map

    def writeString(self, filePath: str):
        # Tried to use a BPM

        log.info("StepMania writeString is not stable on MultiBpm cases!")
        log.info("Start Parsing File")

        header = [
            f"//------{self.chartType}[{self.difficultyVal} {self.difficulty}]------",
            "#NOTES:",
            f"\t{self.chartType}:",
            f"\t{self.description}:",
            f"\t{self.difficulty}:",
            f"\t{self.difficultyVal}:",
            "\t" + ",".join(map(str, self.grooveRadar)) + ":"
        ]

        log.info(f"Header {header}")

        bpmBeats = SMBpmPoint.getBeats(self.bpmPoints, self.bpmPoints)

        # bpmAlign = self.bpmPoints
        # bpmAlign = BpmPoint.alignBpms(self.bpmPoints)
        # bpmBeats = SMBpmPoint.getBeats(bpmAlign, bpmAlign)

        # List[Tuple[Beat, Column], Char]]
        notes: List[List[float, int, str]] = []

        for snap, ho in zip(SMBpmPoint.getBeats(self.hitObjects(), self.bpmPoints), self.hitObjects()):
            notes.append([snap, ho.column, SMHitObject.STRING])

        holdObjectHeads = []
        holdObjectTails = []

        for head, tail in self.holdObjectOffsets(True):
            holdObjectHeads.append(head)
            holdObjectTails.append(tail)

        for snap, ho in zip(SMBpmPoint.getBeats(holdObjectHeads, self.bpmPoints), self.holdObjects()):
            notes.append([snap, ho.column, SMHoldObject.STRING_HEAD])

        for snap, ho in zip(SMBpmPoint.getBeats(holdObjectTails, self.bpmPoints), self.holdObjects()):
            notes.append([snap, ho.column, SMHoldObject.STRING_TAIL])

        del holdObjectHeads, holdObjectTails

        notes.sort(key=lambda x: x[0])

        # BPM Beat 1                     , BPM Beat 2 ...
        # List[List[Beat, Column, Char]], List[List[Beat, Column, Char]]
        notesByBpm: List[List[float, int, str]] = []
        for bpmBeatIndex in range(len(bpmBeats)):
            # If we are at the end, we use infinity as the upper bound
            bpmBeatLower = bpmBeats[bpmBeatIndex]
            bpmBeatUpper = bpmBeats[bpmBeatIndex + 1] if bpmBeatIndex < len(bpmBeats) - 1 else float("inf")

            # Filter out placement for this bpm beat
            noteByBpm: List[List[float, int, str]] = []
            noteIndexToRemove = []
            for noteIndex, note in enumerate(notes):
                # We exclude the any notes are that close to the lower BPM Beat else they will repeat
                if bpmBeatLower - self._SNAP_ERROR_BUFFER <= note[0] < bpmBeatUpper + self._SNAP_ERROR_BUFFER:
                    log.info(f"Note: Beat {round(note[0], 2)}, Column {note[1]}, Char {note[2]} set in "
                             f"{round(bpmBeatLower, 1)} - {round(bpmBeatUpper, 1)}")
                    noteByBpm.append(note)
                    noteIndexToRemove.append(noteIndex)

            # Remove filtered out objects
            noteIndexToRemove.reverse()  # We need to reverse the list to retain correct indexes
            for index in noteIndexToRemove:
                del notes[index]  # faster than pop

            # Zeros the measure and converts it into snap units
            noteByBpm = [[round(m * 48), c, ch] for m, c, ch in noteByBpm]
            notesByBpm += noteByBpm

        del noteByBpm, notes, bpmBeatIndex, bpmBeatUpper, bpmBeatLower, note, noteIndexToRemove, index

        notesByBpm.sort(key=lambda item: item[0])

        measures = [[] for _ in range(int(notesByBpm[-1][0] / 192) + 1)]
        keys = SMMapObjectChartTypes.getKeys(self.chartType)
        for note in notesByBpm:
            measures[int(note[0] / 192)].append(note)

        measuresStr = []
        for measureIndex, measure in enumerate(measures):
            log.info(f"Parse Measure {measureIndex}\t{measure}")
            measure = [[snap % 192, col, char] for snap, col, char in measure]
            log.info(f"Zero Measure\t\t{measure}")
            if len(measure) != 0:
                gcd_ = gcd.reduce([x[0] for x in measure])
                snapsReq: int = int(192 / max(1, gcd_))

                log.info(f"Calc Snaps Req.\t{int(snapsReq)}")
                if snapsReq == 3: snapsReq = 6  # Min 6 snaps to represent
                if snapsReq <  4: snapsReq = 4  # Min 4 snaps to represent
                log.info(f"Final Snaps Req.\t{int(snapsReq)}")

                measure = [[int(snap/(192/snapsReq)), col, char] for snap, col, char in measure]

                measureStr = [['0' for key in range(keys)] for snaps in range(int(snapsReq))]
                log.info(f"Measure Input \t\t{measure}")
                # Note: [Snap, Column, Char]
                for note in measure: measureStr[note[0]][note[1]] = note[2]
            else:
                measureStr = [['0' for key in range(keys)] for snaps in range(4)]
            measuresStr.append("\n".join(["".join(snap) for snap in measureStr]) + f"//{measureIndex}")
            log.info(f"Finished Parsing Measure")

        log.info(f"Finished Parsing Notes")
        return header + ["\n,\n".join(measuresStr)] + [";\n\n"]

    def _readNotes(self, measures: List[List[str]], bpms: List[SMBpmPoint], stops: List[SMStop]):
        globalBeatIndex: float = 0.0  # This will help sync the bpm used
        currentBpmIndex: int = 0
        currentStopIndex: int = -1
        offset = bpms[0].offset
        stopOffsetSum = 0

        bpmBeats = SMBpmPoint.getBeats(bpms, bpms)
        stopBeats = SMBpmPoint.getBeats(stops, bpms)

        holdBuffer: Dict[int, float] = {}
        rollBuffer: Dict[int, float] = {}

        for measure in measures:
            for beatIndex in range(4):
                # Grabs the few snaps in the measure
                beat = measure[int(beatIndex * len(measure) / 4): int((beatIndex + 1) * len(measure) / 4)]

                # Use beat
                for snapIndex, snap in enumerate(beat):
                    for columnIndex, columnChar in enumerate(snap):
                        if columnChar == "0":
                            continue
                        elif columnChar == SMHitObject.STRING:
                            self.noteObjects.append(SMHitObject(offset + stopOffsetSum, column=columnIndex))
                            log.info(f"Read Hit at \t\t{round(offset + stopOffsetSum)} "
                                     f"at Column {columnIndex}")
                        elif columnChar == SMMineObject.STRING:
                            self.noteObjects.append(SMMineObject(offset + stopOffsetSum, column=columnIndex))
                            log.info(f"Read Mine at \t\t{round(offset + stopOffsetSum, 2)} "
                                     f"at Column {columnIndex}")
                        elif columnChar == SMHoldObject.STRING_HEAD:
                            holdBuffer[columnIndex] = offset
                            log.info(f"Read HoldHead at \t{round(offset + stopOffsetSum, 2)} "
                                     f"at Column {columnIndex}")
                        elif columnChar == SMRollObject.STRING_HEAD:
                            rollBuffer[columnIndex] = offset
                            log.info(f"Read RollHead at \t{round(offset + stopOffsetSum, 2)} "
                                     f"at Column {columnIndex}")
                        elif columnChar == SMRollObject.STRING_TAIL:  # ROLL and HOLD tail is the same
                            #  Flush out hold/roll buffer
                            if columnIndex in holdBuffer.keys():
                                startOffset = holdBuffer.pop(columnIndex)
                                self.noteObjects.append(SMHoldObject(startOffset + stopOffsetSum,
                                                                     column=columnIndex,
                                                                     length=offset - startOffset))
                                log.info(f"Read HoldTail at \t{round(startOffset + stopOffsetSum, 2)} "
                                         f"of length {round(offset - startOffset, 2)} "
                                         f"at Column {columnIndex}")
                            elif columnIndex in rollBuffer.keys():
                                startOffset = rollBuffer.pop(columnIndex)
                                self.noteObjects.append(SMRollObject(startOffset + stopOffsetSum,
                                                                     column=columnIndex,
                                                                     length=offset - startOffset))
                                log.info(f"Read RollTail at \t{round(startOffset + stopOffsetSum, 2)} "
                                         f"of length {round(offset - startOffset, 2)} "
                                         f"at Column {columnIndex}")
                        elif columnChar == SMLiftObject.STRING:
                            self.noteObjects.append(SMLiftObject(offset=offset + stopOffsetSum,
                                                                 column=columnIndex))
                            log.info(f"Read Lift at \t\t{round(offset + stopOffsetSum, 2)} "
                                     f"at Column {columnIndex}")
                        elif columnChar == SMFakeObject.STRING:
                            self.noteObjects.append(SMFakeObject(offset=offset + stopOffsetSum,
                                                                 column=columnIndex))
                            log.info(f"Read Fake at \t\t{round(offset + stopOffsetSum, 2)} "
                                     f"at Column {columnIndex}")
                        elif columnChar == SMKeySoundObject.STRING:
                            self.noteObjects.append(SMKeySoundObject(offset=offset + stopOffsetSum,
                                                                     column=columnIndex))
                            log.info(f"Read KeySound at \t{round(offset + stopOffsetSum, 2)} "
                                      f"at Column {columnIndex}")

                    globalBeatIndex += 4.0 / len(measure)
                    offset += bpms[currentBpmIndex].beatLength() / len(beat)
                    #         <-  Fraction  ->   <-    Length of Beat     ->
                    #         Length of Snap

                    # Check if next index exists & check if current beat index is outdated
                    while currentBpmIndex + 1 != len(bpms) and \
                            globalBeatIndex > bpmBeats[currentBpmIndex + 1] - self._SNAP_ERROR_BUFFER:
                        globalBeatIndex = bpmBeats[currentBpmIndex + 1]
                        currentBpmIndex += 1

                        # print(f"Update {bpms[currentBpmIndex - 1].offset + 635 * 2} to "
                        #       f"{bpms[currentBpmIndex].offset + 635 * 2}")

                    # Add stop offsets to current offset sum
                    while currentStopIndex + 1 != len(stops) and \
                            globalBeatIndex > stopBeats[currentStopIndex + 1]:
                        stopOffsetSum += stops[currentStopIndex + 1].length
                        currentStopIndex += 1

                globalBeatIndex = round(globalBeatIndex)

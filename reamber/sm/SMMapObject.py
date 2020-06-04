from __future__ import annotations

from reamber.base.MapObject import MapObject
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

from reamber.sm.mapobj.SMMapObjectBpms import SMMapObjectBpms
from reamber.sm.mapobj.SMMapObjectNotes import SMMapObjectNotes

from dataclasses import dataclass, field
from typing import List, Dict

from numpy import gcd

import logging
log = logging.getLogger(__name__)


@dataclass
class SMMapObject(MapObject, SMMapObjectMeta):

    _SNAP_ERROR_BUFFER = 0.001

    notes: SMMapObjectNotes = field(default_factory=lambda: SMMapObjectNotes())
    bpms:  SMMapObjectBpms  = field(default_factory=lambda: SMMapObjectBpms())

    @staticmethod
    def readString(noteStr: str, bpms: List[SMBpmPoint], stops: List[SMStop]) -> SMMapObject:
        """ Reads the Note part of the SM Map
        That means including the // Comment, and anything below
        :param noteStr: The note part
        :param bpms: BPMs to help sync notes
        :param stops: Stops to help sync notes
        :return:
        """
        spl = noteStr.split(":")
        noteStr = SMMapObject()
        noteStr._readNoteMetadata(spl[1:6])  # These contain the metadata

        # Splits measures by \n and filters out blank + comment entries
        measures: List[List[str]] =\
            [[snap for snap in measure.split("\n")
              if "//" not in snap and len(snap) > 0] for measure in spl[-1].split(",")]

        noteStr._readNotes(measures, bpms=bpms, stops=stops)
        return noteStr

    def writeString(self) -> List[str]:
        """ Write an exportable String List to be passed to SMMapset for writing.
        :return: Exportable String List
        """
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

        bpmBeats = SMBpmPoint.getBeats(self.bpms, self.bpms)

        # -------- We will grab all required notes here --------
        # List[Tuple[Beat, Column], Char]]
        notes: List[List[float, int, str]] = []

        for snap, ho in zip(SMBpmPoint.getBeats(self.notes.hits, self.bpms), self.notes.hits):
            notes.append([snap, ho.column, SMHitObject.STRING])

        holdObjectHeads = []
        holdObjectTails = []

        for head, tail in self.notes.holds.sorted().offsets():
            holdObjectHeads.append(head)
            holdObjectTails.append(tail)

        for snap, ho in zip(SMBpmPoint.getBeats(holdObjectHeads, self.bpms), self.notes.holds):
            assert isinstance(ho, (SMHoldObject, SMRollObject))
            notes.append([snap, ho.column, ho.STRING_HEAD])

        for snap, ho in zip(SMBpmPoint.getBeats(holdObjectTails, self.bpms), self.notes.holds):
            assert isinstance(ho, (SMHoldObject, SMRollObject))
            notes.append([snap, ho.column, SMHoldObject.STRING_TAIL])

        del holdObjectHeads, holdObjectTails

        notes.sort(key=lambda x: x[0])

        # -------- Loop through Bpm --------
        # This is where notes are slot into the BPM beats
        # We loop through the BPMs and find which notes fit
        # We then remove the fitted notes and repeat

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
                    log.info(f"Write Note: Beat {round(note[0], 2)}, Column {note[1]}, Char {note[2]} set in "
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

        # -------- Fit into Measures --------
        # After finding which notes belong to which BPM
        # We cut them into measures then slot them in
        # Note that we want to have the smallest size template before slotting
        # That's where GCD comes in handy.

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
                # Using GCD, we can determine the smallest template to use
                gcd_ = gcd.reduce([x[0] for x in measure])
                if gcd_ == 0: snapsReq: int = 4
                else: snapsReq: int = int(192 / gcd_)

                log.info(f"Calc Snaps Req.\t{int(snapsReq)}")
                if snapsReq == 3: snapsReq = 6  # Min 6 snaps to represent
                if snapsReq < 4: snapsReq = 4  # Min 4 snaps to represent
                log.info(f"Final Snaps Req.\t{int(snapsReq)}")

                # This the template created to slot in notes
                measure = [[int(snap/(192/snapsReq)), col, char] for snap, col, char in measure]

                measureStr = [['0' for _key in range(keys)] for _snaps in range(int(snapsReq))]
                log.info(f"Write Measure Input \t\t{measure}")

                # Note: [Snap, Column, Char]
                for note in measure: measureStr[note[0]][note[1]] = note[2]
            else:
                measureStr = [['0' for _key in range(keys)] for _snaps in range(4)]
            measuresStr.append("\n".join(["".join(snap) for snap in measureStr]) + f"//{measureIndex}")
            log.info(f"Finished Parsing Measure")

        log.info(f"Finished Parsing Notes")
        return header + ["\n,\n".join(measuresStr)] + [";\n\n"]

    def _readNotes(self, measures: List[List[str]], bpms: List[SMBpmPoint], stops: List[SMStop]):
        """ Reads notes from split measures
        We expect a format of [['0000',...]['0100',...]]
        :param measures: Measures as 2D List
        :param bpms: BPMs to help sync
        :param stops: Stops to help Sync
        """
        globalBeatIndex: float = 0.0  # This will help sync the bpm used
        currentBpmIndex: int = 0
        currentStopIndex: int = -1
        offset = bpms[0].offset
        stopOffsetSum = 0

        bpmBeats = SMBpmPoint.getBeats(bpms, bpms)
        stopBeats = SMBpmPoint.getBeats(stops, bpms)

        # The buffer is used to find the head and tails
        # If we find the head, we throw it in here {Col, HeadOffset}
        # If we find the tail, we extract ^ and clear the Dict then form the Hold/Roll
        holdBuffer: Dict[int, float] = {}
        rollBuffer: Dict[int, float] = {}

        for measure in measures:
            for beatIndex in range(4):
                # Grabs the first beat in the measure
                beat = measure[int(beatIndex * len(measure) / 4): int((beatIndex + 1) * len(measure) / 4)]

                # Loop through the beat
                for snapIndex, snap in enumerate(beat):
                    for columnIndex, columnChar in enumerate(snap):
                        # "Switch" statement for character found
                        if columnChar == "0":
                            continue
                        elif columnChar == SMHitObject.STRING:
                            self.notes.hits.append(SMHitObject(offset + stopOffsetSum, column=columnIndex))
                            log.info(f"Read Hit at \t\t{round(offset + stopOffsetSum)} "
                                     f"at Column {columnIndex}")
                        elif columnChar == SMMineObject.STRING:
                            self.notes.hits.append(SMMineObject(offset + stopOffsetSum, column=columnIndex))
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
                                self.notes.holds.append(SMHoldObject(startOffset + stopOffsetSum,
                                                                     column=columnIndex,
                                                                     length=offset - startOffset))
                                log.info(f"Read HoldTail at \t{round(startOffset + stopOffsetSum, 2)} "
                                         f"of length {round(offset - startOffset, 2)} "
                                         f"at Column {columnIndex}")
                            elif columnIndex in rollBuffer.keys():
                                startOffset = rollBuffer.pop(columnIndex)
                                self.notes.holds.append(SMRollObject(startOffset + stopOffsetSum,
                                                                     column=columnIndex,
                                                                     length=offset - startOffset))
                                log.info(f"Read RollTail at \t{round(startOffset + stopOffsetSum, 2)} "
                                         f"of length {round(offset - startOffset, 2)} "
                                         f"at Column {columnIndex}")
                        elif columnChar == SMLiftObject.STRING:
                            self.notes.hits.append(SMLiftObject(offset=offset + stopOffsetSum,
                                                                column=columnIndex))
                            log.info(f"Read Lift at \t\t{round(offset + stopOffsetSum, 2)} "
                                     f"at Column {columnIndex}")
                        elif columnChar == SMFakeObject.STRING:
                            self.notes.hits.append(SMFakeObject(offset=offset + stopOffsetSum,
                                                                column=columnIndex))
                            log.info(f"Read Fake at \t\t{round(offset + stopOffsetSum, 2)} "
                                     f"at Column {columnIndex}")
                        elif columnChar == SMKeySoundObject.STRING:
                            self.notes.hits.append(SMKeySoundObject(offset=offset + stopOffsetSum,
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

                    # Add stop offsets to current offset sum
                    while currentStopIndex + 1 != len(stops) and \
                            globalBeatIndex > stopBeats[currentStopIndex + 1]:
                        stopOffsetSum += stops[currentStopIndex + 1].length
                        currentStopIndex += 1

                # Deal with rounding issues
                globalBeatIndex = round(globalBeatIndex)

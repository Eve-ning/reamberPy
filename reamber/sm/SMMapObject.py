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

from dataclasses import dataclass
from typing import List
from typing import Dict

from math import gcd


@dataclass
class SMMapObject(MapObject, SMMapObjectMeta):

    _SNAP_ERROR_BUFFER = 0.001

    @staticmethod
    def readString(map: str, bpms: List[SMBpmPoint]) -> SMMapObject:
        spl = map.split(":")
        m = SMMapObject()
        m._readNoteMetadata(spl[1:6])  # These contain the metadata

        # Splits measures by \n and filters out blank + comment entries
        measures: List[List[str]] =\
            [[snap for snap in measure.split("\n")
              if "//" not in snap and len(snap) > 0] for measure in spl[-1].split(",")]

        m._readNotes(measures, bpms=bpms)
        return m

    # def recalculateStops(self) -> List[SMStop]:
    #     beats = SMBpmPoint.getBeatsFromTOs(self.bpmPoints, self.bpmPoints)
    #     stops: List[SMStop] = []
    #
    #     for index in range(len(beats) - 1):
    #         if (beats[index + 1] - beats[index]) % 1 != 0.0:
    #             stops.append(SMStop(self.bpmPoints[index + 1].offset,
    #                                 ((beats[index + 1] - beats[index]) % 1)
    #                                 * 60 * 1000 / self.bpmPoints[index + 1].bpm))
    #     return stops

    def writeString(self, filePath: str, FORCE_USE: bool = False):
        # The code doesn't seem to work with multiBPM cases, see Caravan
        # recalculateStops seems to fix Escapes but it breaks Caravan further

        if not FORCE_USE: raise NotImplementedError

        header = [
            f"//------{self.chartType}[{self.difficultyVal} {self.difficulty}]------",
            "#NOTES:",
            f"\t{self.chartType}:",
            f"\t{self.description}:",
            f"\t{self.difficulty}:",
            f"\t{self.difficultyVal}:",
            "\t" + ",".join(map(str, self.grooveRadar)) + ":"
        ]

        bpmBeats = SMBpmPoint.getBeatsFromTOs(self.bpmPoints, self.bpmPoints)

        # List[Tuple[Beat, Column], Char]]
        notes: List[List[float, int, str]] = []

        for snap, ho in zip(SMBpmPoint.getBeatsFromTOs(self.hitObjects(), self.bpmPoints), self.hitObjects()):
            notes.append([snap, ho.column, SMHitObject.STRING])

        holdObjectOffsets = self.holdObjectOffsets()
        holdObjectHeads = []
        holdObjectTails = []

        for head, tail in holdObjectOffsets:
            holdObjectHeads.append(head)
            holdObjectTails.append(tail)

        for snap, ho in zip(SMBpmPoint.getBeatsFromOffsets(holdObjectHeads, self.bpmPoints), self.holdObjects()):
            notes.append([snap, ho.column, SMHoldObject.STRING_HEAD])

        for snap, ho in zip(SMBpmPoint.getBeatsFromOffsets(holdObjectTails, self.bpmPoints), self.holdObjects()):
            notes.append([snap, ho.column, SMHoldObject.STRING_TAIL])

        del holdObjectOffsets, holdObjectHeads, holdObjectTails, head, tail, snap, ho

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
                    noteByBpm.append(note)
                    noteIndexToRemove.append(noteIndex)

            # Remove filtered out objects
            noteIndexToRemove.reverse()  # We need to reverse the list to retain correct indexes
            for index in noteIndexToRemove:
                del notes[index]  # faster than pop

            # Zeros the measure and converts it into snap units
            noteByBpm = [[round((m - (bpmBeatLower % 1)) * 48), c, ch] for m, c, ch in noteByBpm]
            notesByBpm += noteByBpm

        del noteByBpm, notes, bpmBeatIndex, bpmBeatUpper, bpmBeatLower, note, noteIndexToRemove, index

        notesByBpm.sort(key=lambda item: item[0])

        measures = [[] for i in range(int(notesByBpm[-1][0] / 192) + 1)]
        keys = SMMapObjectChartTypes.getKeys(self.chartType)
        for note in notesByBpm:
            measures[int(note[0] / 192)].append(note)

        measuresStr = []
        for measureIndex, measure in enumerate(measures):
            measure = [[snap % 192, col, char] for snap, col, char in measure]
            if len(measure) != 0:
                snapsGcd = gcd.reduce([x[0] for x in measure])

                if snapsGcd == 192 / 3: snapsGcd = 192 / 6  # Min 6 snaps to represent
                if snapsGcd >  192 / 4 or snapsGcd == 0: snapsGcd = 192 / 4  # Min 4 snaps to represent

                measure = [[int(snap / snapsGcd), col, char] for snap, col, char in measure]

                measureStr = [['0' for key in range(keys)] for snaps in range(int(192 / snapsGcd))]

                # Note: [Snap, Column, Char]
                for note in measure:
                    measureStr[note[0]][note[1]] = note[2]
            else:
                measureStr = [['0' for key in range(keys)] for snaps in range(4)]

            measuresStr.append("\n".join(["".join(snap) for snap in measureStr]) + f"//{measureIndex}")

        return header + ["\n,\n".join(measuresStr)] + [";\n\n"]
        # while offsetCurr < offsetLast:

    def _readNotes(self, measures: List[List[str]], bpms: List[SMBpmPoint]):
        globalBeatIndex: float = 0.0  # This will help sync the bpm used
        currentBpmIndex: int = 0
        offset = bpms[0].offset

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
                            self.noteObjects.append(SMHitObject(offset, column=columnIndex))
                        elif columnChar == SMMineObject.STRING:
                            self.noteObjects.append(SMMineObject(offset=offset, column=columnIndex))
                        elif columnChar == SMHoldObject.STRING_HEAD:
                            holdBuffer[columnIndex] = offset
                        elif columnChar == SMRollObject.STRING_HEAD:
                            rollBuffer[columnIndex] = offset
                        elif columnChar == SMRollObject.STRING_TAIL:  # ROLL and HOLD tail is the same
                            #  Flush out hold/roll buffer
                            if columnIndex in holdBuffer.keys():
                                startOffset = holdBuffer.pop(columnIndex)
                                self.noteObjects.append(SMHoldObject(offset=startOffset, column=columnIndex,
                                                                     length=offset - startOffset))
                            elif columnIndex in rollBuffer.keys():
                                startOffset = rollBuffer.pop(columnIndex)
                                self.noteObjects.append(SMRollObject(offset=startOffset, column=columnIndex,
                                                                     length=offset - startOffset))
                        elif columnChar == SMLiftObject.STRING:
                            self.noteObjects.append(SMLiftObject(offset=offset, column=columnIndex))
                        elif columnChar == SMFakeObject.STRING:
                            self.noteObjects.append(SMFakeObject(offset=offset, column=columnIndex))
                        elif columnChar == SMKeySoundObject.STRING:
                            self.noteObjects.append(SMKeySoundObject(offset=offset, column=columnIndex))

                    print(f"{offset + 41*2} : {bpms[currentBpmIndex]}")
                    offset += bpms[currentBpmIndex].beatLength() / len(beat)
                    #         <-  Fraction  ->   <-        Length of Beat        ->
                    #         Length of Snap
                globalBeatIndex += 1

                # Check if next index exists & check if current beat index is outdated
                if currentBpmIndex + 1 != len(bpms) and \
                    globalBeatIndex > bpms[currentBpmIndex + 1].beat - self._SNAP_ERROR_BUFFER:
                    globalBeatIndex = bpms[currentBpmIndex + 1].beat
                    currentBpmIndex += 1

                    # If the difference is significant, add a beat
                    if bpms[currentBpmIndex].beat - bpms[currentBpmIndex - 1].beat > self._SNAP_ERROR_BUFFER:
                        # For some reason a beat is skipped here
                        offset = bpms[currentBpmIndex].offset + bpms[currentBpmIndex].beatLength()

                    # # If there's a double skip, we add to the globalBeatIndex
                    # while currentBpmIndex + 1 != len(bpms) and \
                    #       globalBeatIndex > bpms[currentBpmIndex + 1].beat - self._SNAP_ERROR_BUFFER:
                    #     globalBeatIndex = bpms[currentBpmIndex + 1].beat
                    #     currentBpmIndex += 1
                    #     # For some reason a beat is skipped here
                    #     offset = bpms[currentBpmIndex].offset + bpms[currentBpmIndex].beatLength()
                    # # break  # Do not parse unused snaps




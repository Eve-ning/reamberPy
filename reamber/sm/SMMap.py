from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, TYPE_CHECKING

from reamber.base.Map import Map
from reamber.base.lists import TimedList
from reamber.sm.SMBpm import SMBpm
from reamber.sm.SMConst import SMConst
from reamber.sm.SMFake import SMFake
from reamber.sm.SMHit import SMHit
from reamber.sm.SMHold import SMHold
from reamber.sm.SMKeySound import SMKeySound
from reamber.sm.SMLift import SMLift
from reamber.sm.SMMapMeta import SMMapMeta, SMMapChartTypes
from reamber.sm.SMMine import SMMine
from reamber.sm.SMRoll import SMRoll
from reamber.sm.SMStop import SMStop
from reamber.sm.lists.SMBpmList import SMBpmList
from reamber.sm.lists.SMNotePkg import SMNotePkg

if TYPE_CHECKING:
    from reamber.sm.SMMapSet import SMMapSet

from numpy import gcd

import logging
log = logging.getLogger(__name__)


@dataclass
class SMMap(Map, SMMapMeta):
    """ If you're trying to load using this, use SMMapSet. """

    _SNAP_ERROR_BUFFER = 0.001

    notes: SMNotePkg = field(default_factory=lambda: SMNotePkg())
    bpms:  SMBpmList = field(default_factory=lambda: SMBpmList())

    def data(self) -> Dict[str, TimedList]:
        """ Gets the notes and bpms as a dictionary """
        return {'notes': self.notes,
                'bpms': self.bpms}

    @staticmethod
    def readString(noteStr: str, bpms: List[SMBpm], stops: List[SMStop]) -> SMMap:
        """ Reads the Note part of the SM Map
        That means including the // Comment, and anything below
        :param noteStr: The note part
        :param bpms: BPMs to help sync notes
        :param stops: Stops to help sync notes
        :return:
        """
        spl = noteStr.split(":")
        noteStr = SMMap()
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

        bpmBeats = SMBpm.getBeats(self.bpms, self.bpms)

        # -------- We will grab all required notes here --------
        # List[Tuple[Beat, Column], Char]]
        notes: List[List[float, int, str]] = []

        for snap, ho in zip(SMBpm.getBeats(self.notes.hits(), self.bpms), self.notes.hits()):
            notes.append([snap, ho.column, SMConst.HIT_STRING])

        holdHeads = []
        holdTails = []

        for head, tail in zip(self.notes.holds().sorted().offsets(),self.notes.holds().sorted().tailOffsets()):
            holdHeads.append(head)
            holdTails.append(tail)

        for snap, ho in zip(SMBpm.getBeats(holdHeads, self.bpms), self.notes.holds()):
            if isinstance(ho, SMHold):   notes.append([snap, ho.column, SMConst.HOLD_STRING_HEAD])
            elif isinstance(ho, SMRoll): notes.append([snap, ho.column, SMConst.ROLL_STRING_HEAD])

        for snap, ho in zip(SMBpm.getBeats(holdTails, self.bpms), self.notes.holds()):
            if isinstance(ho, SMHold):   notes.append([snap, ho.column, SMConst.HOLD_STRING_TAIL])
            elif isinstance(ho, SMRoll): notes.append([snap, ho.column, SMConst.ROLL_STRING_TAIL])

        del holdHeads, holdTails

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
        keys = SMMapChartTypes.getKeys(self.chartType)
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
            measuresStr.append("\n".join(["".join(snap) for snap in measureStr]))
            log.info(f"Finished Parsing Measure")

        log.info(f"Finished Parsing Notes")
        return header + ["\n,\n".join(measuresStr)] + [";\n\n"]

    def _readNotes(self, measures: List[List[str]], bpms: List[SMBpm], stops: List[SMStop]):
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

        bpmBeats = SMBpm.getBeats(bpms, bpms)
        stopBeats = SMBpm.getBeats(stops, bpms)

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
                        elif columnChar == SMConst.HIT_STRING:
                            self.notes.hits().append(SMHit(offset + stopOffsetSum, column=columnIndex))
                            log.info(f"Read Hit at \t\t{round(offset + stopOffsetSum)} "
                                     f"at Column {columnIndex}")
                        elif columnChar == SMConst.MINE_STRING:
                            self.notes.hits().append(SMMine(offset + stopOffsetSum, column=columnIndex))
                            log.info(f"Read Mine at \t\t{round(offset + stopOffsetSum, 2)} "
                                     f"at Column {columnIndex}")
                        elif columnChar == SMConst.HOLD_STRING_HEAD:
                            holdBuffer[columnIndex] = offset
                            log.info(f"Read HoldHead at \t{round(offset + stopOffsetSum, 2)} "
                                     f"at Column {columnIndex}")
                        elif columnChar == SMConst.ROLL_STRING_HEAD:
                            rollBuffer[columnIndex] = offset
                            log.info(f"Read RollHead at \t{round(offset + stopOffsetSum, 2)} "
                                     f"at Column {columnIndex}")
                        elif columnChar == SMConst.ROLL_STRING_TAIL:  # ROLL and HOLD tail is the same
                            #  Flush out hold/roll buffer
                            if columnIndex in holdBuffer.keys():
                                startOffset = holdBuffer.pop(columnIndex)
                                self.notes.holds().append(SMHold(startOffset + stopOffsetSum,
                                                                     column=columnIndex,
                                                                     _length=offset - startOffset))
                                log.info(f"Read HoldTail at \t{round(startOffset + stopOffsetSum, 2)} "
                                         f"of length {round(offset - startOffset, 2)} "
                                         f"at Column {columnIndex}")
                            elif columnIndex in rollBuffer.keys():
                                startOffset = rollBuffer.pop(columnIndex)
                                self.notes.holds().append(SMRoll(startOffset + stopOffsetSum,
                                                                     column=columnIndex,
                                                                     _length=offset - startOffset))
                                log.info(f"Read RollTail at \t{round(startOffset + stopOffsetSum, 2)} "
                                         f"of length {round(offset - startOffset, 2)} "
                                         f"at Column {columnIndex}")
                        elif columnChar == SMConst.LIFT_STRING:
                            self.notes.hits().append(SMLift(offset=offset + stopOffsetSum,
                                                                column=columnIndex))
                            log.info(f"Read Lift at \t\t{round(offset + stopOffsetSum, 2)} "
                                     f"at Column {columnIndex}")
                        elif columnChar == SMConst.FAKE_STRING:
                            self.notes.hits().append(SMFake(offset=offset + stopOffsetSum,
                                                                column=columnIndex))
                            log.info(f"Read Fake at \t\t{round(offset + stopOffsetSum, 2)} "
                                     f"at Column {columnIndex}")
                        elif columnChar == SMConst.KEYSOUND_STRING:
                            self.notes.hits().append(SMKeySound(offset=offset + stopOffsetSum,
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

    # noinspection PyMethodOverriding
    # Class requires set to operate
    def metadata(self, s: SMMapSet, unicode=True) -> str:
        """ Grabs the map metadata

        :param s: The Map Set Object, required for additional metadata info.
        :param unicode: Whether to try to find the unicode or non-unicode. \
            This doesn't try to convert unicode to ascii, it just looks for if there's an available translation.
        :return:
        """

        def formatting(artist, title, difficulty, creator):
            return f"{artist} - {title}, {difficulty} ({creator})"

        if unicode:
            return formatting(s.artist if len(s.artist.strip()) > 0 else s.artistTranslit,
                              s.title if len(s.title.strip()) > 0 else s.titleTranslit,
                              self.difficulty, s.credit)
        else:
            return formatting(s.artistTranslit if len(s.artistTranslit.strip()) > 0 else s.artist,
                              s.titleTranslit if len(s.titleTranslit.strip()) > 0 else s.title,
                              self.difficulty, s.credit)

    # noinspection PyMethodOverriding
    def describe(self, s:SMMapSet, rounding: int = 2, unicode: bool = False) -> None:
        """ Describes the map's attributes as a short summary

        :param s: The Map Set Object, required for additional metadata info.
        :param rounding: The decimal rounding
        :param unicode: Whether to attempt to get the non-unicode or unicode. \
            Doesn't attempt to translate.
        """
        super(SMMap, self).describe(rounding=rounding, unicode=unicode, s=s)

    def rate(self, by: float, inplace:bool = False):
        """ Changes the rate of the map. Note that you need to do rate on the mapset to correctly affect the sm output

        :param by: The value to rate it by. 1.1x speeds up the song by 10%. Hence 10/11 of the length.
        :param inplace: Whether to perform the operation in place. Returns a copy if False
        """
        # Sample start and length aren't changed here.
        return super(SMMap, self).rate(by=by, inplace=inplace)

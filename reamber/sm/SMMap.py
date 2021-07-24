from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, TYPE_CHECKING

from reamber.base.Map import Map
from reamber.base.Property import map_props
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
from reamber.sm.lists.notes import SMNoteList, SMHitList, SMHoldList, SMFakeList, SMLiftList, SMKeySoundList, \
    SMMineList, SMRollList

if TYPE_CHECKING:
    from reamber.sm.SMMapSet import SMMapSet

from numpy import gcd

import logging
log = logging.getLogger(__name__)


@map_props()
@dataclass
class SMMap(Map[SMNoteList, SMHitList, SMHoldList, SMBpmList], SMMapMeta):
    """ If you're trying to load using this, use SMMapSet. """

    _props = dict(fakes=SMFakeList,
                  lifts=SMLiftList,
                  keysounds=SMKeySoundList,
                  mines=SMMineList,
                  rolls=SMRollList)

    _SNAP_ERROR_BUFFER = 0.001

    @staticmethod
    def read_string(note_str: str, bpms: SMBpmList, stops: List[SMStop]) -> SMMap:
        """ Reads the Note part of the SM Map
        That means including the // Comment, and anything below
        :param note_str: The note part
        :param bpms: BPMs to help sync notes
        :param stops: Stops to help sync notes
        :return:
        """
        spl = note_str.split(":")
        note_str = SMMap(objects=[SMHitList([]), SMHoldList([]), SMFakeList([]), SMKeySoundList([]), SMMineList([]),
                                  SMRollList([]), SMLiftList([]), SMBpmList([])])
        note_str._read_note_metadata(spl[1:6])  # These contain the metadata

        # Splits measures by \n and filters out blank + comment entries
        measures: List[List[str]] =\
            [[snap for snap in measure.split("\n")
              if "//" not in snap and len(snap) > 0] for measure in spl[-1].split(",")]

        note_str._read_notes(measures, bpms=bpms, stops=stops)
        return note_str

    def write_string(self) -> List[str]:
        """ Write an exportable String List to be passed to SMMapset for writing.
        :return: Exportable String List
        """
        # Tried to use a BPM

        log.info("StepMania writeString is not stable on MultiBpm cases!")
        log.info("Start Parsing File")

        header = [
            f"//------{self.chart_type}[{self.difficulty_val} {self.difficulty}]------",
            "#NOTES:",
            f"\t{self.chart_type}:",
            f"\t{self.description}:",
            f"\t{self.difficulty}:",
            f"\t{self.difficulty_val}:",
            "\t" + ",".join(map(str, self.groove_radar)) + ":"
        ]

        log.info(f"Header {header}")

        bpm_beats = SMBpm.get_beats(self.bpms, self.bpms)

        # -------- We will grab all required notes here --------
        # List[Tuple[Beat, Column], Char]]
        notes: List[List[float, int, str]] = []

        for snap, ho in zip(SMBpm.get_beats(self.hits, self.bpms), self.hits):
            notes.append([snap, ho.column, SMConst.HIT_STRING])

        hold_heads = []
        hold_tails = []

        for head, tail in zip(self.holds.sorted().offset, self.holds.sorted().tail_offset):
            hold_heads.append(head)
            hold_tails.append(tail)

        for snap, ho in zip(SMBpm.get_beats(hold_heads, self.bpms), self.holds):
            if isinstance(ho, SMHold):   notes.append([snap, ho.column, SMConst.HOLD_STRING_HEAD])
            elif isinstance(ho, SMRoll): notes.append([snap, ho.column, SMConst.ROLL_STRING_HEAD])

        for snap, ho in zip(SMBpm.get_beats(hold_tails, self.bpms), self.holds):
            if isinstance(ho, SMHold):   notes.append([snap, ho.column, SMConst.HOLD_STRING_TAIL])
            elif isinstance(ho, SMRoll): notes.append([snap, ho.column, SMConst.ROLL_STRING_TAIL])

        del hold_heads, hold_tails

        notes.sort(key=lambda x: x[0])

        # -------- Loop through Bpm --------
        # This is where notes are slot into the BPM beats
        # We loop through the BPMs and find which notes fit
        # We then remove the fitted notes and repeat

        # BPM Beat 1                     , BPM Beat 2 ...
        # List[List[Beat, Column, Char]], List[List[Beat, Column, Char]]
        notes_by_bpm: List[List[float, int, str]] = []
        for bpm_beat_index in range(len(bpm_beats)):
            # If we are at the end, we use infinity as the upper bound
            bpm_beat_lower = bpm_beats[bpm_beat_index]
            bpm_beat_upper = bpm_beats[bpm_beat_index + 1] if bpm_beat_index < len(bpm_beats) - 1 else float("inf")

            # Filter out placement for this bpm beat
            note_by_bpm: List[List[float, int, str]] = []
            note_index_to_remove = []
            for noteIndex, note in enumerate(notes):
                # We exclude the any notes are that close to the lower BPM Beat else they will repeat
                if bpm_beat_lower - self._SNAP_ERROR_BUFFER <= note[0] < bpm_beat_upper + self._SNAP_ERROR_BUFFER:
                    log.info(f"Write Note: Beat {round(note[0], 2)}, Column {note[1]}, Char {note[2]} set in "
                             f"{round(bpm_beat_lower, 1)} - {round(bpm_beat_upper, 1)}")
                    note_by_bpm.append(note)
                    note_index_to_remove.append(noteIndex)

            # Remove filtered out objects
            note_index_to_remove.reverse()  # We need to reverse the list to retain correct indexes
            for index in note_index_to_remove:
                del notes[index]  # faster than pop

            # Zeros the measure and converts it into snap units
            note_by_bpm = [[round(m * 48), c, ch] for m, c, ch in note_by_bpm]
            notes_by_bpm += note_by_bpm

        del note_by_bpm, notes, bpm_beat_index, bpm_beat_upper, bpm_beat_lower, note, note_index_to_remove, index

        notes_by_bpm.sort(key=lambda item: item[0])

        # -------- Fit into Measures --------
        # After finding which notes belong to which BPM
        # We cut them into measures then slot them in
        # Note that we want to have the smallest size template before slotting
        # That's where GCD comes in handy.

        measures = [[] for _ in range(int(notes_by_bpm[-1][0] / 192) + 1)]
        keys = SMMapChartTypes.get_keys(self.chart_type)
        for note in notes_by_bpm:
            measures[int(note[0] / 192)].append(note)

        measures_str = []
        for measure_index, measure in enumerate(measures):
            log.info(f"Parse Measure {measure_index}\t{measure}")
            measure = [[snap % 192, col, char] for snap, col, char in measure]
            log.info(f"Zero Measure\t\t{measure}")
            if len(measure) != 0:
                # Using GCD, we can determine the smallest template to use
                gcd_ = gcd.reduce([x[0] for x in measure])
                if gcd_ == 0: snaps_req: int = 4
                else: snaps_req: int = int(192 / gcd_)

                log.info(f"Calc Snaps Req.\t{int(snaps_req)}")
                if snaps_req == 3: snaps_req = 6  # Min 6 snaps to represent
                if snaps_req < 4: snaps_req = 4  # Min 4 snaps to represent
                log.info(f"Final Snaps Req.\t{int(snaps_req)}")

                # This the template created to slot in notes
                measure = [[int(snap/(192/snaps_req)), col, char] for snap, col, char in measure]

                measure_str = [['0' for _key in range(keys)] for _snaps in range(int(snaps_req))]
                log.info(f"Write Measure Input \t\t{measure}")

                # Note: [Snap, Column, Char]
                for note in measure: measure_str[note[0]][note[1]] = note[2]
            else:
                measure_str = [['0' for _key in range(keys)] for _snaps in range(4)]
            measures_str.append("\n".join(["".join(snap) for snap in measure_str]))
            log.info(f"Finished Parsing Measure")

        log.info(f"Finished Parsing Notes")
        return header + ["\n,\n".join(measures_str)] + [";\n\n"]

    def _read_notes(self, measures: List[List[str]], bpms: SMBpmList, stops: List[SMStop]):
        """ Reads notes from split measures
        We expect a format of [['0000',...]['0100',...]]
        :param measures: Measures as 2D List
        :param bpms: BPMs to help sync
        :param stops: Stops to help Sync
        """
        global_beat_index: float = 0.0  # This will help sync the bpm used
        current_bpm_index: int = 0
        current_stop_index: int = -1
        offset = bpms[0].offset
        stop_offset_sum = 0

        bpm_beats = SMBpm.get_beats(bpms, bpms)
        stop_beats = SMBpm.get_beats(stops, bpms)

        # The buffer is used to find the head and tails
        # If we find the head, we throw it in here {Col, HeadOffset}
        # If we find the tail, we extract ^ and clear the Dict then form the Hold/Roll
        hold_buffer: Dict[int, float] = {}
        roll_buffer: Dict[int, float] = {}

        hits, holds, fakes, lifts, keysounds, mines, rolls = [], [], [], [], [], [], []

        for measure in measures:
            for beat_index in range(4):
                # Grabs the first beat in the measure
                beat = measure[int(beat_index * len(measure) / 4): int((beat_index + 1) * len(measure) / 4)]

                # Loop through the beat
                for snap_index, snap in enumerate(beat):
                    for column_index, column_char in enumerate(snap):
                        # "Switch" statement for character found
                        if column_char == "0": continue
                        elif column_char == SMConst.HIT_STRING:
                            hits.append(SMHit(offset + stop_offset_sum, column=column_index))
                            log.info(f"Read Hit at \t\t{round(offset + stop_offset_sum)} "
                                     f"at Column {column_index}")
                        elif column_char == SMConst.MINE_STRING:
                            mines.append(SMMine(offset + stop_offset_sum, column=column_index))
                            log.info(f"Read Mine at \t\t{round(offset + stop_offset_sum, 2)} "
                                     f"at Column {column_index}")
                        elif column_char == SMConst.HOLD_STRING_HEAD:
                            # TODO: Verify if it's + stop_offset_sum or just offset ?
                            hold_buffer[column_index] = offset + stop_offset_sum
                            log.info(f"Read HoldHead at \t{round(offset + stop_offset_sum, 2)} "
                                     f"at Column {column_index}")
                        elif column_char == SMConst.ROLL_STRING_HEAD:
                            roll_buffer[column_index] = offset + stop_offset_sum
                            log.info(f"Read RollHead at \t{round(offset + stop_offset_sum, 2)} "
                                     f"at Column {column_index}")
                        elif column_char == SMConst.ROLL_STRING_TAIL:  # ROLL and HOLD tail is the same
                            #  Flush out hold/roll buffer
                            if column_index in hold_buffer.keys():
                                start_offset = hold_buffer.pop(column_index)
                                holds.append(SMHold(start_offset + stop_offset_sum,
                                                    column=column_index,
                                                    length=offset - start_offset))
                                log.info(f"Read HoldTail at \t{round(start_offset + stop_offset_sum, 2)} "
                                         f"of length {round(offset - start_offset, 2)} "
                                         f"at Column {column_index}")
                            elif column_index in roll_buffer.keys():
                                start_offset = roll_buffer.pop(column_index)
                                rolls.append(SMRoll(start_offset + stop_offset_sum,
                                                    column=column_index,
                                                    length=offset - start_offset))
                                log.info(f"Read RollTail at \t{round(start_offset + stop_offset_sum, 2)} "
                                         f"of length {round(offset - start_offset, 2)} "
                                         f"at Column {column_index}")
                        elif column_char == SMConst.LIFT_STRING:
                            lifts.append(SMLift(offset=offset + stop_offset_sum,
                                                column=column_index))
                            log.info(f"Read Lift at \t\t{round(offset + stop_offset_sum, 2)} "
                                     f"at Column {column_index}")
                        elif column_char == SMConst.FAKE_STRING:
                            fakes.append(SMFake(offset=offset + stop_offset_sum,
                                                column=column_index))
                            log.info(f"Read Fake at \t\t{round(offset + stop_offset_sum, 2)} "
                                     f"at Column {column_index}")
                        elif column_char == SMConst.KEYSOUND_STRING:
                            keysounds.append(SMKeySound(offset=offset + stop_offset_sum,
                                                        column=column_index))
                            log.info(f"Read KeySound at \t{round(offset + stop_offset_sum, 2)} "
                                     f"at Column {column_index}")

                    global_beat_index += 4.0 / len(measure)
                    offset += bpms[current_bpm_index].beat_length / len(beat)
                    #         <-  Fraction  ->   <-    Length of Beat     ->
                    #         Length of Snap

                    # Check if next index exists & check if current beat index is outdated
                    while current_bpm_index + 1 != len(bpms) and \
                            global_beat_index > bpm_beats[current_bpm_index + 1] - self._SNAP_ERROR_BUFFER:
                        global_beat_index = bpm_beats[current_bpm_index + 1]
                        current_bpm_index += 1

                    # Add stop offsets to current offset sum
                    while current_stop_index + 1 != len(stops) and \
                            global_beat_index > stop_beats[current_stop_index + 1]:
                        stop_offset_sum += stops[current_stop_index + 1].length
                        current_stop_index += 1

                # Deal with rounding issues
                global_beat_index = round(global_beat_index)

        self.hits      = SMHitList(hits)
        self.holds     = SMHoldList(holds)
        self.fakes     = SMFakeList(fakes)
        self.lifts     = SMLiftList(lifts)
        self.keysounds = SMKeySoundList(keysounds)
        self.mines     = SMMineList(mines)
        self.rolls     = SMRollList(rolls)

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
            return formatting(s.artist if len(s.artist.strip()) > 0 else s.artist_translit,
                              s.title if len(s.title.strip()) > 0 else s.title_translit,
                              self.difficulty, s.credit)
        else:
            return formatting(s.artist_translit if len(s.artist_translit.strip()) > 0 else s.artist,
                              s.title_translit if len(s.title_translit.strip()) > 0 else s.title,
                              self.difficulty, s.credit)

    # noinspection PyMethodOverriding
    def describe(self, s:SMMapSet, rounding: int = 2, unicode: bool = False):
        """ Describes the map's attributes as a short summary

        :param s: The Map Set Object, required for additional metadata info.
        :param rounding: The decimal rounding
        :param unicode: Whether to attempt to get the non-unicode or unicode. \
            Doesn't attempt to translate.
        """
        return super().describe(rounding=rounding, unicode=unicode, s=s)

    def rate(self, by: float):
        """ Changes the rate of the map. Note that you need to do rate on the mapset to correctly affect the sm output

        :param by: The value to rate it by. 1.1x speeds up the song by 10%. Hence 10/11 of the length.
        """
        # Sample start and length aren't changed here.
        return super().rate(by=by)

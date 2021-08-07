from __future__ import annotations

from collections import namedtuple
from dataclasses import dataclass, field
from typing import List, TYPE_CHECKING, Union, Dict

from reamber.base.Map import Map
from reamber.base.Property import map_props
from reamber.base.lists.TimedList import TimedList
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
from reamber.sm.lists.SMStopList import SMStopList
from reamber.sm.lists.notes import SMNoteList, SMHitList, SMHoldList, SMFakeList, SMLiftList, SMKeySoundList, \
    SMMineList, SMRollList

if TYPE_CHECKING:
    from reamber.sm.SMMapSet import SMMapSet

from numpy import gcd

import logging
log = logging.getLogger(__name__)

DEFAULT_BEAT_PER_MEASURE = 4
MAX_KEYS = 18

@map_props()
@dataclass
class SMMap(Map[SMNoteList, SMHitList, SMHoldList, SMBpmList], SMMapMeta):
    """ If you're trying to load using this, use SMMapSet. """

    _props = dict(fakes=SMFakeList,
                  lifts=SMLiftList,
                  keysounds=SMKeySoundList,
                  mines=SMMineList,
                  rolls=SMRollList,
                  stops=SMStopList)
    objs: Dict[str, TimedList] = \
        field(init=False,
              default_factory=lambda: dict(fakes=SMFakeList([]),
                                           lifts=SMLiftList([]),
                                           keysounds=SMKeySoundList([]),
                                           mines=SMMineList([]),
                                           rolls=SMRollList([]),
                                           stops=SMStopList([]),
                                           hits=SMHitList([]),
                                           holds=SMHoldList([]),
                                           bpms=SMBpmList([])))
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
        sm = SMMap()
        sm.bpms = bpms
        sm.stops = stops
        sm._read_note_metadata(spl[1:6])  # These contain the metadata

        # Splits measures by \n and filters out blank + comment entries
        measures: List[List[str]] =\
            [[snap for snap in measure.split("\n")
              if "//" not in snap and len(snap) > 0] for measure in spl[-1].split(",")]

        sm._read_notes(measures)
        return sm

    def write_string(self) -> List[str]:
        """ Write an exportable String List to be passed to SMMapset for writing.
        :return: Exportable String List
        """

        header = [
            f"//------{self.chart_type}[{self.difficulty_val} {self.difficulty}]------",
            "#NOTES:",
            f"     {self.chart_type}:",
            f"     {self.description}:",
            f"     {self.difficulty}:",
            f"     {self.difficulty_val}:",
            "     " + ",".join(map(str, self.groove_radar)) + ":"
        ]

        def beats(offsets):
            return [SMBpm.mbs_to_beat(*i) for i in tm.snaps(offsets, transpose=True)]

        tm = self.bpms.to_timing_map()
        bpm_beats = beats(self.bpms.offset)

        # -------- We will grab all required notes here --------
        # List[Tuple[Beat, Column], Char]]

        notes = \
            [beats(
                [*self.hits.offset,
                 *self.holds.head_offset,
                 *self.holds.tail_offset,
                 *self.rolls.head_offset,
                 *self.rolls.tail_offset,
                 *self.fakes.offset,
                 *self.keysounds.offset,
                 *self.lifts.offset,
                 *self.mines.offset]
            ),
             [*self.hits.column,
              *self.holds.column,
              *self.holds.column,
              *self.rolls.column,
              *self.rolls.column,
              *self.fakes.column,
              *self.keysounds.column,
              *self.lifts.column,
              *self.mines.column],
             [*[SMConst.HIT_STRING] * len(self.hits),
              *[SMConst.HOLD_STRING_HEAD] * len(self.holds),
              *[SMConst.HOLD_STRING_TAIL] * len(self.holds),
              *[SMConst.ROLL_STRING_HEAD] * len(self.rolls),
              *[SMConst.ROLL_STRING_TAIL] * len(self.rolls),
              *[SMConst.FAKE_STRING] * len(self.fakes),
              *[SMConst.KEYSOUND_STRING] * len(self.keysounds),
              *[SMConst.LIFT_STRING] * len(self.lifts),
              *[SMConst.MINE_STRING] * len(self.mines)]
            ]
        notes = list(zip(*notes))
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
            # noinspection PyTypeChecker
            note_by_bpm: List[List[float, int, str]] = []
            note_index_to_remove = []
            for note_index, note in enumerate(notes):
                # We exclude the any notes are that close to the lower BPM Beat else they will repeat
                if bpm_beat_lower - self._SNAP_ERROR_BUFFER <= note[0] < bpm_beat_upper + self._SNAP_ERROR_BUFFER:
                    log.info(f"Write Note: Beat {round(note[0], 2)}, Column {note[1]}, Char {note[2]} set in "
                             f"{round(bpm_beat_lower, 1)} - {round(bpm_beat_upper, 1)}")
                    # noinspection PyTypeChecker
                    note_by_bpm.append(note)
                    note_index_to_remove.append(note_index)

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
                # noinspection PyUnresolvedReferences
                gcd_ = gcd.reduce([int(x[0]) for x in measure])
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
                for note in measure: measure_str[int(note[0])][int(note[1])] = note[2]
            else:
                measure_str = [['0' for _key in range(keys)] for _snaps in range(4)]
            measures_str.append("\n".join(["".join(snap) for snap in measure_str]))
            log.info(f"Finished Parsing Measure")

        log.info(f"Finished Parsing Notes")
        return header + ["\n,\n".join(measures_str)] + [";\n\n"]

    def _read_notes(self, measures: List[List[str]]):
        """ Reads notes from split measures
        We expect a format of [['0000',...]['0100',...]]
        :param measures: Measures as 2D List
        """

        Hit      = namedtuple('Hit',      ['measure', 'beat', 'slot'])
        Hold     = namedtuple('Hold',     ['head', 'tail'])

        tm = self.bpms.to_timing_map()

        hits      : List[List[Hit]]              = [[] for _ in range(MAX_KEYS)]
        lifts     : List[List[Hit]]              = [[] for _ in range(MAX_KEYS)]
        mines     : List[List[Hit]]              = [[] for _ in range(MAX_KEYS)]
        fakes     : List[List[Hit]]              = [[] for _ in range(MAX_KEYS)]
        key_sounds: List[List[Hit]]              = [[] for _ in range(MAX_KEYS)]
        holds     : List[List[Union[Hold, Hit]]] = [[] for _ in range(MAX_KEYS)]
        rolls     : List[List[Union[Hold, Hit]]] = [[] for _ in range(MAX_KEYS)]

        for measure, measure_str in enumerate(measures):
            for beat in range(4):
                beat_str = measure_str[int(beat * len(measure_str) / 4): int((beat + 1) * len(measure_str) / 4)]
                # Loop through the beat
                for snap, snap_str in enumerate(beat_str):
                    snap /= len(beat_str)
                    for col, col_char in enumerate(snap_str):
                        # "Switch" statement for character found
                        if col_char == "0": continue
                        obj = Hit(measure, beat, snap)

                        if col_char == SMConst.HIT_STRING: hits[col].append(obj)
                        elif col_char == SMConst.MINE_STRING: mines[col].append(obj)
                        elif col_char == SMConst.HOLD_STRING_HEAD: holds[col].append(obj)
                        elif col_char == SMConst.ROLL_STRING_HEAD: rolls[col].append(obj)
                        elif col_char == SMConst.ROLL_STRING_TAIL:  # ROLL and HOLD tail is the same
                            try:
                                if isinstance(holds[col][-1], Hit):
                                    holds[col][-1] = Hold(holds[col][-1], obj)
                                else: raise IndexError()
                            except IndexError:
                                try:
                                    if isinstance(rolls[col][-1], Hit):
                                        rolls[col][-1] = Hold(rolls[col][-1], obj)
                                    else: raise IndexError()
                                except IndexError:
                                    raise IndexError("Hold or Roll didn't match column specified.")
                        elif col_char == SMConst.LIFT_STRING: lifts[col].append(obj)
                        elif col_char == SMConst.FAKE_STRING: fakes[col].append(obj)
                        elif col_char == SMConst.KEYSOUND_STRING: key_sounds[col].append(obj)

        # noinspection PyShadowingNames
        def _expand(objs, cls):
            objs_ = []
            for key_, i_ in enumerate(objs):
                if not i_: continue
                objs_.extend([cls(offset, key_)
                              for offset in tm.offsets(*list(zip(*[(obj.measure, obj.beat, obj.slot) for obj in i_])))])
            return objs_

        # noinspection PyShadowingNames
        def _expand_hold(objs, cls):
            objs_ = []
            for key_, i_ in enumerate(objs):
                if not i_: continue
                head = tm.offsets(*list(zip(*[(obj.head.measure, obj.head.beat, obj.head.slot,) for obj in i_])))
                tail = tm.offsets(*list(zip(*[(obj.tail.measure, obj.tail.beat, obj.tail.slot,) for obj in i_])))
                objs_.extend([cls(h, key_, t - h) for h, t in zip(head, tail)])
            return objs_

        self.hits      = SMHitList(_expand(hits, SMHit))
        self.holds     = SMHoldList(_expand_hold(holds, SMHold))
        self.fakes     = SMFakeList(_expand(fakes, SMFake))
        self.lifts     = SMLiftList(_expand(lifts, SMLift))
        self.keysounds = SMKeySoundList(_expand(key_sounds, SMKeySound))
        self.mines     = SMMineList(_expand(mines, SMMine))
        self.rolls     = SMRollList(_expand_hold(rolls, SMRoll))

        # TODO: Band-aid fix, not sure why we need to shift by a beat?
        #  It is due to stops, but is this consistent?
        #  The case is that, for every stop, we need to shift anything beyond that stop by a beat of the associated bpm.
        for stop in self.stops.sorted(True):
            shift = self.bpms.current_bpm(stop.offset).beat_length
            for objs in (self.hits, self.holds, self.fakes, self.lifts, self.keysounds, self.mines, self.rolls):
                # noinspection PyTypeChecker
                objs.offset[objs.offset >= stop.offset] += shift

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

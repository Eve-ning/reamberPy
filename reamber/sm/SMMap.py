from __future__ import annotations

from collections import namedtuple
from dataclasses import dataclass, field
from fractions import Fraction
from typing import List, TYPE_CHECKING, Union, Dict

import numpy as np
import pandas as pd

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
            return [SMBpm.mbs_to_beat(*i) for i in tm.snaps(offsets, divisions=(1,2,3,4,5,6,7,8,9,10,12,16,32,48),
                                                            transpose=True)]

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
        notes = pd.DataFrame(list(zip(*notes)), columns=['beat', 'column', 'char'])
        notes['measure'] = notes.beat // DEFAULT_BEAT_PER_MEASURE
        notes['den'] = [i.denominator for i in notes.beat]
        notes['num'] = [i.numerator for i in notes.beat]

        notes.den *= DEFAULT_BEAT_PER_MEASURE
        notes.num %= notes.den

        notes_gb = notes.groupby('measure')
        out = []
        for _, g in notes_gb:
            den_max = g.den.max()
            lines = [['0' for i in range(SMMapChartTypes.get_keys(self.chart_type))] for j in range(den_max)]
            g.num *= den_max / g.den
            g.num = g.num.astype(int)
            g.column = g.column.astype(int)
            for _, note in g.iterrows():
                lines[note.num][note.column] = note.char
            out.append("\n".join(["".join(line) for line in lines]))

        return header + ["\n,\n".join(out)] + [";\n\n"]

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
                              for offset in tm.offsets(*list(zip(*[(obj.measure, obj.beat, obj.division) for obj in i_])))])
            return objs_

        # noinspection PyShadowingNames
        def _expand_hold(objs, cls):
            objs_ = []
            for key_, i_ in enumerate(objs):
                if not i_: continue
                head = tm.offsets(*list(zip(*[(obj.head.measure, obj.head.beat, obj.head.division,) for obj in i_])))
                tail = tm.offsets(*list(zip(*[(obj.tail.measure, obj.tail.beat, obj.tail.division,) for obj in i_])))
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

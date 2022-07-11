from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from functools import reduce
from typing import List, TYPE_CHECKING, Dict, Tuple

import numpy as np
import pandas as pd

from reamber.algorithms.timing.TimingMap import TimingMap
from reamber.algorithms.timing.utils.BpmChangeSnap import BpmChangeSnap
from reamber.algorithms.timing.utils.Snapper import Snapper
from reamber.algorithms.timing.utils.snap import Snap
from reamber.base.Map import Map
from reamber.base.Property import map_props
from reamber.base.lists.TimedList import TimedList
from reamber.sm.SMBpm import SMBpm
from reamber.sm.SMConst import SMConst
from reamber.sm.SMMapMeta import SMMapMeta, SMMapChartTypes
from reamber.sm.lists.SMBpmList import SMBpmList
from reamber.sm.lists.SMStopList import SMStopList
from reamber.sm.lists.notes import SMNoteList, SMHitList, SMHoldList, \
    SMFakeList, SMLiftList, SMKeySoundList, \
    SMMineList, SMRollList

if TYPE_CHECKING:
    from reamber.sm.SMMapSet import SMMapSet

METRONOME = 4
MAX_SNAP = 384
MAX_KEYS = 18


@map_props()
@dataclass
class SMMap(Map[SMNoteList, SMHitList, SMHoldList, SMBpmList], SMMapMeta):
    # If you're trying to load using this, use SMMapSet.

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

    @staticmethod
    def read(s: str,
             bcs_s: List[BpmChangeSnap],
             initial_offset: float,
             stops: SMStopList) -> SMMap:
        """Reads the Notes section of the SM Map

        Args:
            s: string of the section
            bcs_s: Bpm Change Snaps from metadata
            initial_offset: Initial offset from metadata
            stops: Stops from metadata

        Returns:
            A Parsed SMMap
        """
        _, *note_metadata, note_data = s.split(":")
        sm = SMMap()
        sm._read_note_metadata(note_metadata)  # Metadata of each map in mapset
        sm._read_notes(note_data, initial_offset, bcs_s, stops)
        return sm

    def write(self) -> List[str]:
        """Writes a map as a String List for SMMapset to write. """

        header = [
            f"//------{self.chart_type}"
            f"[{self.difficulty_val} {self.difficulty}]------",
            "#NOTES:",
            f"     {self.chart_type}:",
            f"     {self.description}:",
            f"     {self.difficulty}:",
            f"     {self.difficulty_val}:",
            "     " + ",".join(map(str, self.groove_radar)) + ":"
        ]

        tm = self.bpms.to_timing_map()
        snapper = Snapper()
        notes = \
            [tm.beats(
                [*self.hits.offset,
                 *self.holds.head_offset,
                 *self.holds.tail_offset,
                 *self.rolls.head_offset,
                 *self.rolls.tail_offset,
                 *self.fakes.offset,
                 *self.keysounds.offset,
                 *self.lifts.offset,
                 *self.mines.offset], snapper=snapper
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
        notes = pd.DataFrame(list(zip(*notes)),
                             columns=['beat', 'column', 'char'])
        notes['measure'] = notes.beat // METRONOME
        notes['den'] = [i.denominator for i in notes.beat]
        notes['num'] = [i.numerator for i in notes.beat]

        notes.den *= METRONOME
        notes.num %= notes.den

        notes_gb = notes.groupby('measure')
        out = []
        keys = SMMapChartTypes.get_keys(self.chart_type)

        def lcm_and_cap(x, y):
            """LCMs and dynamically caps the result to MAX_SNAP"""
            return min(np.lcm(x, y), MAX_SNAP)

        # Helps track measures to fill empty measures
        prev_measure = -1
        for measure, g in notes_gb:
            # As we only use measures that exist, we skip those that don't
            # We add those as padded 0000s.
            for _ in range(measure - prev_measure - 1):
                out.append("\n".join(['0000'] * METRONOME))
            prev_measure = measure

            # We find maximum LCM denominator that works for all snaps
            den_max = min(reduce(lcm_and_cap, g.den), MAX_SNAP)

            lines = [['0' for _ in range(keys)] for __ in range(den_max)]

            g.num *= den_max / g.den
            g.num = g.num.astype(int)
            g.column = g.column.astype(int)

            for note in g.itertuples():
                lines[note.num][note.column] = note.char

            out.append("\n".join(["".join(line) for line in lines]))

        return header + ["\n,\n".join(out)] + [";\n\n"]

    def _read_notes(self,
                    note_data: str,
                    initial_offset: float,
                    bcs_s: List[BpmChangeSnap],
                    stops: SMStopList):
        """Reads notes section from split measures. Excluding Metadata

        Args:
            note_data: Note string, excluding metadata
            initial_offset: Offset from metadata
            bcs_s: Bpm Changes from metadata
            stops: Stops from metadata
        """

        # Split measures by \n and filters out blank + comment entries
        note_data: List[List[str]] = \
            [
                [snap for snap in measure.split("\n")
                 if "//" not in snap and snap]
                for measure in note_data.split(",")
            ]

        tm = TimingMap.from_bpm_changes_snap(initial_offset, bcs_s, False)
        tm_reseat = TimingMap.from_bpm_changes_snap(initial_offset, bcs_s)
        self.bpms = SMBpmList(
            [SMBpm(b.offset, b.bpm) for b in tm_reseat.bpm_changes_offset]
        )
        hits: List[List[Snap]] = [[] for _ in range(MAX_KEYS)]
        lifts: List[List[Snap]] = [[] for _ in range(MAX_KEYS)]
        mines: List[List[Snap]] = [[] for _ in range(MAX_KEYS)]
        fakes: List[List[Snap]] = [[] for _ in range(MAX_KEYS)]
        key_sounds: List[List[Snap]] = [[] for _ in range(MAX_KEYS)]
        holds: List[List[Tuple[Snap, Snap] | Snap]] = [[] for _ in
                                                       range(MAX_KEYS)]
        rolls: List[List[Tuple[Snap, Snap] | Snap]] = [[] for _ in
                                                       range(MAX_KEYS)]

        # Store snap history for quick lookup
        snap_set = set()

        for measure, measure_str in enumerate(note_data):
            for beat in range(METRONOME):
                beat_str = measure_str[
                           int(beat * len(measure_str) / METRONOME):
                           int((beat + 1) * len(measure_str) / METRONOME)
                           ]
                for snap, snap_str in enumerate(beat_str):
                    snap = Fraction(snap, len(beat_str))
                    for col, col_char in enumerate(snap_str):
                        if col_char == "0": continue
                        snap_obj = Snap(measure, beat + snap, METRONOME)

                        # "Switch" statement for character found
                        if col_char == SMConst.HIT_STRING:
                            hits[col].append(snap_obj)
                        elif col_char == SMConst.MINE_STRING:
                            mines[col].append(snap_obj)
                        elif col_char == SMConst.HOLD_STRING_HEAD:
                            holds[col].append(snap_obj)
                        elif col_char == SMConst.ROLL_STRING_HEAD:
                            rolls[col].append(snap_obj)
                            # ROLL and HOLD tail is the same
                        elif col_char == SMConst.ROLL_STRING_TAIL:
                            if holds[col] and isinstance(holds[col][-1], Snap):
                                holds[col][-1] = holds[col][-1], snap_obj
                            elif (
                                rolls[col] and isinstance(rolls[col][-1], Snap)
                            ):
                                rolls[col][-1] = rolls[col][-1], snap_obj
                            else:
                                raise IndexError(
                                    "Hold/Roll failed to find head note"
                                )
                        elif col_char == SMConst.LIFT_STRING:
                            lifts[col].append(snap_obj)
                        elif col_char == SMConst.FAKE_STRING:
                            fakes[col].append(snap_obj)
                        elif col_char == SMConst.KEYSOUND_STRING:
                            key_sounds[col].append(snap_obj)
                        snap_set.add(snap_obj)

        snap_set = list(snap_set)
        snap_mapping = {k: v for k, v in
                        zip(snap_set, tm.offsets(snap_set))}

        # noinspection PyShadowingNames
        def _expand(snaps_s: List[List[Snap]]):
            objs = []
            for k, snaps in enumerate(snaps_s):
                objs.extend([dict(offset=offset, column=k)
                             for offset in map(snap_mapping.get, snaps)])
            return objs

        # noinspection PyShadowingNames
        def _expand_hold(snaps_s: List[List[Tuple[Snap, Snap]]]):
            objs = []
            for k, snaps_ht in enumerate(snaps_s):
                if not snaps_ht: continue
                snaps_h, snaps_t = list(zip(*snaps_ht))
                head = map(snap_mapping.get, snaps_h)
                tail = map(snap_mapping.get, snaps_t)
                objs.extend([dict(offset=h, column=k, length=t - h)
                             for h, t in zip(head, tail)])
            return objs

        self.hits = SMHitList.from_dict(_expand(hits))
        self.holds = SMHoldList.from_dict(_expand_hold(holds))
        self.fakes = SMFakeList.from_dict(_expand(fakes))
        self.lifts = SMLiftList.from_dict(_expand(lifts))
        self.keysounds = SMKeySoundList.from_dict(_expand(key_sounds))
        self.mines = SMMineList.from_dict(_expand(mines))
        self.rolls = SMRollList.from_dict(_expand_hold(rolls))

        for stop in stops.sorted(True):
            for objs in (self.hits, self.holds, self.fakes, self.lifts,
                         self.keysounds, self.mines, self.rolls):
                # TODO: Band-aid fix, unsure of + stop.length, but it works on
                #  Escapes for now.
                #  Might have to do with how the note & stop interacts.
                # noinspection PyTypeChecker
                objs.loc[objs.offset >= (stop.offset + stop.length),
                         'offset'] += stop.length

    # noinspection PyMethodOverriding
    def metadata(self, ms: SMMapSet, unicode=True) -> str:
        """Grabs the map metadata

        Args:
            ms: The Map Set Object, required for additional metadata info.
            unicode: Whether to use unicode translate if available.
        """

        fmt = "{} - {}, {} ({})"
        if unicode:
            return fmt.format(
                ms.artist if ms.artist.strip() else ms.artist_translit,
                ms.title if ms.title.strip() else ms.title_translit,
                self.difficulty,
                ms.credit
            )
        else:
            return fmt.format(
                (ms.artist_translit if ms.artist_translit.strip()
                 else ms.artist),
                ms.title_translit if ms.title_translit.strip() else ms.title,
                self.difficulty,
                ms.credit
            )

    # noinspection PyMethodOverriding
    def describe(self, ms: SMMapSet, rounding: int = 2, unicode: bool = False):
        """Describes the map's attributes as a short summary

        Args:
            ms: The Map Set Object, required for additional metadata info.
            rounding: The decimal rounding
            unicode: Whether to use unicode translate if available.
        """
        return super().describe(rounding=rounding, unicode=unicode, s=ms)

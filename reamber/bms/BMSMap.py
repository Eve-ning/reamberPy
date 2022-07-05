from __future__ import annotations

import logging
import warnings
from codecs import encode, open as codecs_open
from collections import namedtuple
from dataclasses import dataclass, field
from fractions import Fraction
from typing import List, Dict

import numpy as np
import pandas as pd
from numpy import base_repr

from reamber.algorithms.timing import TimingMap
from reamber.algorithms.timing.utils.BpmChangeOffset import BpmChangeOffset
from reamber.algorithms.timing.utils.BpmChangeSnap import BpmChangeSnap
from reamber.algorithms.timing.utils.Snapper import Snapper
from reamber.algorithms.timing.utils.find_lcm import find_lcm
from reamber.algorithms.timing.utils.snap import Snap
from reamber.base.Map import Map
from reamber.base.Property import map_props, stack_props
from reamber.base.lists.TimedList import TimedList
from reamber.bms import BMSHit, BMSHold
from reamber.bms.BMSBpm import BMSBpm
from reamber.bms.BMSChannel import BMSChannel
from reamber.bms.BMSMapMeta import BMSMapMeta
from reamber.bms.lists import BMSBpmList
from reamber.bms.lists.notes import BMSNoteList, BMSHitList, BMSHoldList

MERGE_DELTA = 0.0001

log = logging.getLogger(__name__)
ENCODING = "shift_jis"

DEFAULT_METRONOME = 4
MAX_KEYS = 18


@map_props()
@dataclass
class BMSMap(Map[BMSNoteList, BMSHitList, BMSHoldList, BMSBpmList],
             BMSMapMeta):
    objs: Dict[str, TimedList] = \
        field(init=False,
              default_factory=lambda: dict(hits=BMSHitList([]),
                                           holds=BMSHoldList([]),
                                           bpms=BMSBpmList([])))

    @staticmethod
    def read(lines: List[str],
             note_channel_config: dict = BMSChannel.BME) -> BMSMap:
        """ Reads from a list of strings

        Notes:
            Channel config determines channel-column mapping

        Args:
            lines: List of strings from the file
            note_channel_config: Get this config from reamber.bms.BMSChannel
                If unsure, use the default BME.
        """

        header = {}
        notes = []
        bms = BMSMap()

        lines = [line.strip() for line in lines]  # Redundancy for safety

        for line in lines:
            # Check if it's a command
            if line.startswith('#'):
                # We split it by b' '.
                # If it's size == 2, then it's a header metadata
                # Else, it may be an unfilled header or a note data.

                # Sometimes titles have spaces, so we split maximum of once.
                line_split = line.encode('shift_jis').strip().split(b' ', 1)

                if len(line_split) == 2:
                    # Header Metadata (Filled)
                    log.debug(f"Add {line_split[0][1:]}: "
                              f"{line_split[1]} header entry")

                    # [1:] Remove the #
                    header[line_split[0][1:]] = line_split[1]

                elif len(line_split) == 1:
                    # ASCII for numbers
                    if ord('0') <= line_split[0][1] <= ord('9'):
                        # Is note
                        command, data = line_split[0].split(b':')
                        measure = command[1:4]
                        channel = command[4:6]
                        sequence = data

                        log.debug(f"Added {measure}, {channel}, "
                                  f"{sequence} note entry")

                        notes.append(dict(measure=measure, channel=channel,
                                          sequence=sequence))

        bms._read_file_header(header)
        bms._read_notes(notes, note_channel_config)
        return bms

    @staticmethod
    def read_file(file_path: str,
                  note_channel_config: dict = BMSChannel.BME) -> BMSMap:
        """ Reads the file

        Notes:
            Channel config determines channel-column mapping

        Args:
            file_path: Path to file
            note_channel_config: Get this config from reamber.bms.BMSChannel
                If unsure, use the default BME.
        """
        with codecs_open(file_path, mode="r", encoding=ENCODING) as f:
            lines = [line.strip() for line in f.readlines()]

        return BMSMap.read(lines, note_channel_config=note_channel_config)

    def write(self,
              note_channel_config: dict = BMSChannel.BME,
              no_sample_default: bytes = b'01'):
        out = b''
        out += self._write_file_header()
        out += b'\r\n' * 2
        out += self._write_notes(note_channel_config=note_channel_config,
                                 no_sample_default=no_sample_default)
        return out

    def write_file(self, file_path: str,
                   note_channel_config: dict = BMSChannel.BME,
                   no_sample_default: bytes = b'01'):
        """ Writes the notes according to self data

        Args:
            file_path: Path to write to
            note_channel_config: The config from BMSChannel
            no_sample_default: The default byte to use when there's no sample
        """
        with open(file_path, "wb+") as f:
            f.write(self.write(note_channel_config=note_channel_config,
                               no_sample_default=no_sample_default))

    def _read_file_header(self, data: dict):
        self.artist = data.get(b'ARTIST', "")
        self.title = data.get(b'TITLE', "")
        self.version = data.get(b'PLAYLEVEL', "")
        self.ln_end_channel = data.get(b'LNOBJ', b'')

        # We cannot pop during a loop, so we save the keys then pop later.
        to_pop = []
        for k, v in data.items():
            if k.upper().startswith(b'BPM') and len(k) == 5:
                self.exbpms[k[3:]] = float(v)
                to_pop.append(k)

        for k, v in data.items():
            if k.upper().startswith(b'WAV'):
                self.samples[k[-2:]] = v
                to_pop.append(k)

        for k in to_pop:
            data.pop(k)

        # We do this to go in-line with the 
        # temporary measure property assigned in _readNotes.
        bpm = BMSBpm(0, bpm=float(data.pop(b'BPM')))

        log.debug(f"Added initial BPM {bpm.bpm}")
        self.bpms = self.bpms.append(bpm)

        self.misc = data

    def _write_file_header(self) -> bytes:
        # May need to change all header stuff to a byte string first.

        # noinspection PyTypeChecker
        title = b"#TITLE " + (encode(self.title, ENCODING)
                              if not isinstance(self.title,
                                                bytes) else self.title)

        # noinspection PyTypeChecker
        artist = b"#ARTIST " + (encode(self.artist, ENCODING)
                                if not isinstance(self.artist,
                                                  bytes) else self.artist)

        bpm = b"#BPM " + encode(str(self.bpms[0].bpm), ENCODING)

        # noinspection PyTypeChecker
        play_level = b"#PLAYLEVEL " + (
            encode(self.version)
            if not isinstance(self.version, bytes) else self.version
        )
        misc = []
        for k, v in self.misc.items():
            k = encode(k, ENCODING) if not isinstance(k, bytes) else k
            v = encode(v, ENCODING) if not isinstance(v, bytes) else v
            misc.append(b'#' + k + b' ' + v)

        ln_obj = b''
        if self.ln_end_channel:
            # noinspection PyTypeChecker
            ln_obj = b"#LNOBJ " + (
                encode(self.ln_end_channel, ENCODING)
                if not isinstance(self.ln_end_channel, bytes)
                else self.ln_end_channel
            )

        assert len(self.bpms) < 35 * 36 + 35, \
            f"The writer doesn't support more than {35 * 36 + 35} BPMs."

        exbpms = []
        for e, b in enumerate(self.bpms, 1):
            exbpms.append(b'#BPM' + bytes(base_repr(e, 36).zfill(2), 'ascii') +
                          b' ' + bytes(f"{b.bpm:.3f}", 'ascii'))

        wavs = []
        for k, v in self.samples.items():
            k = encode(k, ENCODING) if not isinstance(k, bytes) else k
            v = encode(v, ENCODING) if not isinstance(v, bytes) else v
            wavs.append(b'#WAV' + k + b' ' + v)

        return b'\r\n'.join(
            [title, artist, bpm, play_level, *misc, ln_obj, *exbpms, *wavs]
        )

    def _read_notes(self, data: List[dict], config: dict):
        """ The data will be in the format [{measure, channel, seq}, ...]

        This function helps .read
        """

        Hit = namedtuple('Hit', ['sample', 'snap'])
        Hold = namedtuple('Hold', ['hit', 'sample', 'snap'])

        bcs_s = [
            BpmChangeSnap(
                self.bpms[0].bpm, DEFAULT_METRONOME,
                Snap(0, 0, DEFAULT_METRONOME),
            )
        ]
        hits = [[] for _ in range(MAX_KEYS)]
        holds = [[] for _ in range(MAX_KEYS)]
        time_sig = {}

        # The time_sig channel call does not sustain for more than 1 measure.
        # Hence, if the time_sig changes, it's only for that measure.
        # Thus, if the time_sig changes, it'll need correction
        # for the next measure if needed.

        for d in data:
            measure = int(d['measure'])
            channel = d['channel']
            sequence = d['sequence']
            pairs = [sequence[i:i + 2] for i in range(0, len(sequence), 2)]

            if channel == BMSChannel.TIME_SIG:
                # Time Signatures always appear before BPM Changes
                metronome = float(sequence) * DEFAULT_METRONOME
                time_sig[measure] = metronome
            else:
                division = len(sequence) // 2

                # If the latest BPM is of the same measure,
                # this indicates that a TIME_SIG happened on the same measure
                # We will force the current measure to use the changed time sig
                metronome = time_sig.get(measure, DEFAULT_METRONOME)
                for i, pair in enumerate(pairs):
                    if pair == b'00' or pair == b'0': continue

                    beat = Fraction(i, division) * metronome
                    if channel == BMSChannel.BPM_CHANGE or \
                        channel == BMSChannel.EXBPM_CHANGE:
                        new_bpm = (
                            int(pair, 16) if channel == BMSChannel.BPM_CHANGE
                            else float(self.exbpms[pair])
                        )
                        bcs_s.append(
                            BpmChangeSnap(
                                bpm=new_bpm,
                                snap=Snap(measure, beat, metronome),
                                metronome=metronome)
                        )
                    elif channel in config.keys():
                        column = int(config[channel])

                        if pair == self.ln_end_channel:
                            try:
                                # Yield LN Head from Hits
                                prev_hit = hits[column].pop(-1)
                                holds[column].append(
                                    Hold(hit=prev_hit, sample=prev_hit.sample,
                                         snap=Snap(measure, beat, None))
                                )
                            except IndexError:
                                raise Exception(f"Failed to match LN Tail on "
                                                f"Column {column}.")
                        else:
                            # Else it's a note
                            sample = self.samples.get(pair, b'')
                            hits[column].append(
                                Hit(sample=sample,
                                    snap=Snap(measure, beat, None))
                            )
        #
        # measures = [*time_sig.keys(), -1]
        # for measure0, measure1 in zip(measures[:-1], measures[1:]):
        #     if measure1 - measure0 != 1:
        #         time_sig[measure0 + 1] = DEFAULT_METRONOME
        #
        # for measure, metronome in sorted(time_sig.items(), key=lambda x: x[0]):
        #     bcs_measure = []
        #     bcs_last_ix = 0
        #     for e, bcs in enumerate(bcs_s):
        #         if bcs.snap.measure == measure:
        #             bcs_measure.append(bcs)
        #         elif bcs.snap.measure > measure:
        #             bcs_last_ix = e
        #             break
        #
        #     for bcs in bcs_measure:
        #         bcs.metronome = metronome
        #         bcs.snap.metronome = metronome
        # if not bcs_measure:
        #     if bcs_last_ix == 0:
        #         continue
        #     bcs_prev = bcs_s[bcs_last_ix - 1]
        #     bcs_s.insert(
        #         bcs_last_ix,
        #         BpmChangeSnap(bcs_prev.bpm, metronome,
        #                       Snap(measure, 0, metronome))
        #     )

        if len(bcs_s) > 1 and \
            bcs_s[1].snap.measure == 0 and \
            bcs_s[1].snap.beat == 0:
            # Special case:
            # A Measure 0 Beat 0 BPM Change: overriding the global BPM
            bcs_s.pop(0)

        """ Here we have to correct the lack of default metronome resets. 

        The problem is that BMS' time sig changes are only for the current 
        measure, on the contrary, we assume it carries forward to the next 
        measures.

        The algorithm loops all changes and adds an additional time sig 
        change if the previous is non-normal and the current is lacking a reset
        """

        bcs_s.sort(key=lambda x: x.snap)

        tm = TimingMap.from_bpm_changes_snap(
            initial_offset=0, bcs_s=bcs_s, reseat=False
        )

        if any(hits):
            cols, samples, snaps = list(
                zip(*[(k, h.sample, h.snap)
                      for k, hits_col in enumerate(hits)
                      for h in hits_col])
            )

            # TODO: Change offsets to accept multiple args to optimize this

            offsets = tm.offsets(snaps)

            self.hits = BMSHitList([
                BMSHit(sample=sample, offset=offset, column=col)
                for col, sample, offset in zip(cols, samples, offsets)
            ])
        else:
            self.hits = BMSHitList([])

        if any(holds):
            cols, samples, snaps_head, snaps_tail = \
                list(zip(*[(k, h.sample, h.hit.snap, h.snap)
                           for k, holds_col in enumerate(holds)
                           for h in holds_col]))
            offsets_head = tm.offsets(snaps_head)
            offsets_tail = tm.offsets(snaps_tail)

            self.holds = BMSHoldList(
                [BMSHold(sample=sample, offset=head_offset, column=col,
                         length=tail_offset - head_offset)
                 for sample, col, head_offset, tail_offset in
                 zip(samples, cols, offsets_head, offsets_tail)]
            )
        else:
            self.holds = BMSHoldList([])

        tm = tm.reseat()
        self.bpms = BMSBpmList(
            [BMSBpm(offset=b.offset, bpm=b.bpm, metronome=b.metronome)
             for b in tm.bpm_changes_offset]
        )

    def _write_notes(self,
                     note_channel_config: dict,
                     no_sample_default: bytes = b'01'):

        """ Writes the notes according to self data

        Args:
            note_channel_config: The config from BMSChannel
            no_sample_default: The default byte to use when there's no sample
        """
        warnings.warn("Maps with many BPM Changes will likely break this. "
                      "Open up an Issue to support this fully.")
        tm = TimingMap.from_bpm_changes_offset([
            BpmChangeOffset(bpm=b.bpm, metronome=b.metronome,
                            offset=b.offset) for b in self.bpms])

        sample_map = {v: k for k, v in self.samples.items()}
        channel_map = {v: k for k, v in note_channel_config.items()}

        metronome_changes = [b for b in self.bpms if b.metronome != 4]

        """ Find the objects we want to snap here """
        snapper = Snapper()
        hits = [
            (offset, column, sample_map.get(sample, no_sample_default))
            for offset, column, sample in
            zip(tm.snaps(self.hits.offset, snapper),
                self.hits.column, self.hits.sample)
        ]
        holds = [
            (offset, tail_offset, column,
             sample_map.get(sample, no_sample_default))
            for offset, tail_offset, column, sample in
            zip(tm.snaps(self.holds.offset, snapper),
                tm.snaps(self.holds.tail_offset, snapper),
                self.holds.column, self.holds.sample)
        ]

        # BPM Changes
        bpms = [(bytes(base_repr(e + 1, 36).zfill(2), 'ascii'),
                 channel_map["EXBPM_CHANGE"]) for e in range(len(self.bpms))],

        # Metronome Changes
        time_sigs = [
            (bytes(f"{float(m.metronome) / DEFAULT_METRONOME:.4f}", 'ascii'),
             channel_map["TIME_SIG"]) for m in metronome_changes
        ]

        """ Since the objects there are in tuples, we just loop and index 
        
        Make the time signatures to be on beat so that it's render is
        the float.

        This works because seq = b['00'] is replaced with seq = b['sig'] and 
        renders as 'sig'
        """

        """ Here, we find the beats per measure associated for each measure

        This algorithm takes the BPM Metronomes and maps to a integer space: 
        0, 1, 2, ..., n        
        Note that all BPMs WILL BE ON MEASURES, this is because we reparsed the
        BPM, which adds corrections to make all on measures.

        Then, this will forward fill (FF) the Metronomes.

        E.g.

        MEASURE  0  1  2  3  4  5
        METRON   4  -  3  -  4  5
        FFMETRON 4  4  3  3  4  5 ...

        With this, we can allocate all notes their respective Metronome 
        (important for writing).

        """
        # We are only interested in the beats per measure in BMS
        # measure_ar = np.array([b.measure for b in tm.bpm_changes_offset])
        # beats_ar = np.array([b.metronome for b in tm.bpm_changes_offset])
        # measure_mapping_ar = np.empty([int(np.max(df.measure) + 1)])
        # measure_mapping_ar[:] = np.nan
        # measure_mapping_ar[measure_ar] = beats_ar
        # measure_mapping_df = pd.DataFrame(
        #     measure_mapping_ar).ffill().reset_index()
        # measure_mapping_df.columns = ['measure', 'beats_per_measure']
        # df = pd.merge(df, measure_mapping_df, on=['measure'])

        """ Here, we calculate the expected position of the objects. 

        Note that time_sigs don't have position, we circumvented this by making
        the beat and slot 0. """

        # Get expected relative position [0,1]
        # df['position'] = (df.slot + df.beat) / df.beats_per_measure
        #
        # # Slot to possible slots
        # s = TimingMap.Slotter()
        # df['position'] = [s.division(i) for i in df.position]
        # df['position_den'] = [i.denominator for i in df.position]

        """ This step here reduces the denominator such that it's as compact
        as possible.

        E.g.

        MEASURE 0: Note on 3/4, Note on 3/8.
        This algorithm will detect that this is reducable to 6/8 and 3/8, this
        makes it compact when writing out. 

        E.g.

        MEASURE 0: Note on 3/4, Note on 5/6.
        This algorithm will try to reduce to a limit of 100. That means, if we
        can represent both in the same line,
        with a character limit of 100, then we will.
        In this case, it can reduce to 9/12, 10/12. 12 < 100, so this is a
        reducable. 

        """
        df_lcm = df[['measure', 'channel', 'position_den']].groupby(
            ['measure', 'channel'], as_index=False)
        for ix, df_ in df_lcm:
            # noinspection PyProtectedMember
            a = find_lcm(list(df_.position_den), 100)
            mask = (df.measure == ix[0]) & (df.channel == ix[1])
            df.loc[mask, 'position_den'] = a
        df.position *= df.position_den

        """ Write out here. """

        # Generate the lines here
        df = df.sort_values('channel')
        df_out = df[['measure', 'channel', 'position_den', 'position',
                     'sample']].groupby(
            ['measure', 'channel', 'position_den'], as_index=False)
        out = []
        for ix, df_ in df_out:
            line = bytes(f'#{ix[0]:03}', 'ascii') + ix[1] + b':'
            seq = [b'00'] * ix[2]
            df_: pd.DataFrame
            for s in df_.iterrows():
                seq[int(s[1].position)] = s[1]['sample']
            line += b''.join(seq)
            out.append(line)

        return b'\r\n'.join(out)

    # noinspection PyMethodOverriding
    def metadata(self, **kwargs) -> str:
        """ Grabs the map metadata """
        fmt = "{} - {}, {}"
        return fmt.format(self.artist, self.title, self.version)

    @stack_props()
    class Stacker(Map.Stacker):
        _props = ["sample"]

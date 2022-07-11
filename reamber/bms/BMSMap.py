from __future__ import annotations

import logging
import warnings
from codecs import encode, open as codecs_open
from collections import namedtuple
from dataclasses import dataclass, field
from fractions import Fraction
from typing import List, Dict

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
        """Reads from a list of strings

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
        """Reads the file

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
              no_sample_default: bytes = b'01') -> bytes:
        b = b''
        b += self._write_file_header()
        b += b'\r\n' * 2
        b += self._write_notes(note_channel_config=note_channel_config,
                               no_sample_default=no_sample_default)
        return b

    def write_file(self, file_path: str,
                   note_channel_config: dict = BMSChannel.BME,
                   no_sample_default: bytes = b'01'):
        """Writes the notes according to self data

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
        """The data will be in the format [{measure, channel, seq}, ...]

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

        config_rev = {v: k for k, v in config.items()}
        for d in data:
            measure = int(d['measure'])
            channel = d['channel']
            sequence = d['sequence']
            pairs = [sequence[i:i + 2] for i in range(0, len(sequence), 2)]

            if channel == config_rev['TIME_SIG']:
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
                    if channel in (config_rev['BPM_CHANGE'],
                                   config_rev['EXBPM_CHANGE']):
                        new_bpm = (
                            int(pair, 16)
                            if channel == config_rev['BPM_CHANGE']
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
        # for measure, metronome in sorted(time_sig.items(),
        #                                  key=lambda x: x[0]):
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

        if (
            len(bcs_s) > 1 and
            bcs_s[1].snap.measure == 0 and
            bcs_s[1].snap.beat == 0
        ):
            # Special case:
            # A Measure 0 Beat 0 BPM Change: overriding the global BPM
            bcs_s.pop(0)

        # Here we have to correct the lack of default metronome resets.
        # The problem is that BMS' time sig changes are only for the current
        # measure, on the contrary, we assume it carries forward to the next
        # measures.
        # The algorithm loops all changes and adds a time sig
        # change if the prev is non-normal and the current is lacking a reset

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
        """Writes the notes according to self data

        Args:
            note_channel_config: The config from BMSChannel
            no_sample_default: The default byte to use when there's no sample
        """
        warnings.warn("Maps with many BPM Changes will likely break this.")

        tm = TimingMap.from_bpm_changes_offset([
            BpmChangeOffset(bpm=b.bpm, metronome=b.metronome,
                            offset=b.offset) for b in self.bpms])

        sample_map = {v: k for k, v in self.samples.items()}
        channel_map = {v: k for k, v in note_channel_config.items()}

        metronome_changes = [b for b in self.bpms if b.metronome != 4]

        """Find the objects we want to snap here"""
        snapper = Snapper()
        hits = [
            (snap, channel_map[column],
             sample_map.get(sample, no_sample_default))
            for snap, column, sample in
            zip(tm.snaps(self.hits.offset, snapper),
                self.hits.column, self.hits.sample)
        ]

        hold_heads = [
            (snap, channel_map[column],
             sample_map.get(sample, no_sample_default))
            for snap, column, sample in
            zip(tm.snaps(self.holds.offset, snapper),
                self.holds.column, self.holds.sample)
        ]

        hold_tails = [
            (snap, channel_map[column], self.ln_end_channel)
            for snap, column in
            zip(tm.snaps(self.holds.tail_offset, snapper),
                self.holds.column)
        ]

        # BPM Changes
        bpms = [(snap,
                 channel_map["EXBPM_CHANGE"],
                 bytes(base_repr(e + 1, 36).zfill(2), 'ascii'))
                for e, snap in enumerate(tm.snaps(self.bpms.offset, snapper))]

        # Metronome Changes
        time_sigs = [
            (snap,
             channel_map["TIME_SIG"],
             bytes(f"{float(m.metronome) / DEFAULT_METRONOME:.4f}", 'ascii'))
            for snap, m in
            zip(tm.snaps([m.offset for m in metronome_changes], snapper),
                metronome_changes)
        ]

        df = pd.DataFrame(
            [*hits, *hold_heads, *hold_tails, *bpms, *time_sigs],
            columns=['snap', 'channel', 'value']
        )
        df['measure'] = [i.measure for i in df['snap']]
        df['den'] = [i.beat.denominator * i.metronome for i in df['snap']]
        df['num'] = [i.beat.numerator for i in df['snap']]
        df['den'] = df['den'].astype(int)
        df['num'] = df['num'].astype(int)
        df = df.drop(['snap'], axis=1)
        df['new_den'] = 0
        for (measure, channel), dfg in df.groupby(['measure', 'channel']):
            df.loc[(df.measure == measure) & (df.channel == channel),
                   'new_den'] = find_lcm(dfg['den'].tolist(), 100)
        df.num *= df.new_den / df.den
        df = df.drop(['den'], axis=1)

        # Generate the lines here
        df = df.sort_values('channel')
        dfgs = df.groupby(['measure', 'channel', 'new_den'])
        lines = []
        for (measure, channel, den), dfg in dfgs:
            line = bytes(f'#{int(measure):03}', 'ascii') + channel + b':'
            seq = [b'00'] * den
            for _, row in dfg.iterrows():
                seq[int(row['num'])] = row['value']
            line += b''.join(seq)
            lines.append(line)

        return b'\r\n'.join(lines)

    # noinspection PyMethodOverriding
    def metadata(self, **kwargs) -> str:
        """Grabs the map metadata"""
        fmt = "{} - {}, {}"
        return fmt.format(self.artist, self.title, self.version)

    @stack_props()
    class Stacker(Map.Stacker):
        _props = ["sample"]

from __future__ import annotations

import codecs
import logging
from collections import namedtuple
from dataclasses import dataclass, field
from fractions import Fraction
from typing import List, Dict

import numpy as np
import pandas as pd
from numpy import base_repr

from reamber.base.Map import Map
from reamber.base.lists.TimedList import TimedList
from reamber.bms import BMSHit, BMSHold
from reamber.bms.BMSBpm import BMSBpm
from reamber.bms.BMSChannel import BMSChannel
from reamber.bms.BMSMapMeta import BMSMapMeta
from reamber.bms.lists.BMSBpmList import BMSBpmList
from reamber.bms.lists.BMSNotePkg import BMSNotePkg
from reamber.algorithms.timing import TimingMap, BpmChangeSnap, BpmChangeOffset

log = logging.getLogger(__name__)
ENCODING = "shift_jis"

DEFAULT_BEAT_PER_MEASURE = 4
MAX_KEYS = 18

@dataclass
class BMSMap(Map, BMSMapMeta):

    notes: BMSNotePkg = field(default_factory=lambda: BMSNotePkg())
    bpms:  BMSBpmList = field(default_factory=lambda: BMSBpmList())
    _tm: TimingMap = field(init=False)

    @staticmethod
    def read(lines: List[str], note_channel_config: dict = BMSChannel.BME) -> BMSMap:
        """ Reads from a list of strings, depending on the config, keys may change

        If unsure, use the default BME. If all channels don't work please report an issue with it with the file

        The Channel config determines which channel goes to which keys, that means using the wrong channel config
        may scramble the notes.

        :param lines: List of strings from the file
        :param note_channel_config: Get this config from reamber.bms.BMSChannel
        :return:
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
                    log.debug(f"Added {line_split[0][1:]}: {line_split[1]} header entry")
                    # [1:] Remove the #
                    header[line_split[0][1:]] = line_split[1]

                elif len(line_split) == 1:
                    if ord('0') <= line_split[0][1] <= ord('9'):  # ASCII for numbers
                        # Is note
                        command, data = line_split[0].split(b':')
                        measure = command[1:4]
                        channel = command[4:6]
                        sequence = data

                        log.debug(f"Added {measure}, {channel}, {sequence} note entry")
                        notes.append(dict(measure=measure, channel=channel, sequence=sequence))
                    else:
                        # Header Data (Unfilled) <Ignored>
                        pass
                else:
                    # Unexpected data.
                    pass

        bms._read_file_header(header)
        bms._read_notes(notes, note_channel_config)

        return bms

    @staticmethod
    def read_file(filePath: str, note_channel_config: dict = BMSChannel.BME) -> BMSMap:
        """ Reads the file, depending on the config, keys may change

        If unsure, use the default BME. If all channels don't work please report an issue with it with the file

        The Channel config determines which channel goes to which keys, that means using the wrong channel config
        may scramble the notes.

        :param filePath: Path to file
        :param note_channel_config: Get this config from reamber.bms.BMSChannel
        :return:
        """
        with codecs.open(filePath, mode="r", encoding=ENCODING) as f:
            lines = [line.strip() for line in f.readlines()]

        return BMSMap.read(lines, note_channel_config=note_channel_config)

    def write_file(self, file_path,
                   note_channel_config: dict = BMSChannel.BME,
                   no_sample_default: bytes = b'01'):
        """ Writes the notes according to self data

        :param file_path: Path to write to
        :param note_channel_config: The config from BMSChannel
        :param no_sample_default: The default byte to use when there's no sample
        :return:
        """
        with open(file_path, "wb+") as f:
            f.write(self._write_file_header())
            f.write(b'\r\n' * 2)
            f.write(self._write_notes(note_channel_config=note_channel_config, no_sample_default=no_sample_default))

    def _read_file_header(self, data: dict):
        self.artist         = data.pop(b'ARTIST')     if b'ARTIST'    in data.keys() else ""
        self.title          = data.pop(b'TITLE')      if b'TITLE'     in data.keys() else ""
        self.version        = data.pop(b'PLAYLEVEL')  if b'PLAYLEVEL' in data.keys() else ""
        self.ln_end_channel = data.pop(b'LNOBJ')      if b'LNOBJ'     in data.keys() else b''

        # We cannot pop during a loop, so we save the keys then pop later.
        to_pop = []
        for k, v in data.items():
            k: bytes
            if k.startswith(b'BPM') and len(k) == 5:
                self.exbpms[k[3:]] = float(v)
                to_pop.append(k)

        for k, v in data.items():
            if k[:3] == b'WAV':
                self.samples[k[-2:]] = v
                to_pop.append(k)

        for k in to_pop:
            data.pop(k)

        # We do this to go in-line with the temporary measure property assigned in _readNotes.
        bpm = BMSBpm(0, bpm=float(data.pop(b'BPM')))

        log.debug(f"Added initial BPM {bpm.bpm}")
        self.bpms.append(bpm)

        self.misc = data

    def _write_file_header(self) -> bytes:
        # May need to change all header stuff to a byte string first.

        # noinspection PyTypeChecker
        title = b"#TITLE " + (codecs.encode(self.title, ENCODING)
                             if not isinstance(self.title, bytes) else self.title)

        # noinspection PyTypeChecker
        artist = b"#ARTIST " + (codecs.encode(self.artist, ENCODING)
                               if not isinstance(self.artist, bytes) else self.artist)

        bpm = b"#BPM " + codecs.encode(self.bpms[0].bpm, ENCODING)

        # noinspection PyTypeChecker
        playLevel = b"#PLAYLEVEL " + (codecs.encode(self.version)
                                     if not isinstance(self.version, bytes) else self.version)
        misc = []
        for k, v in self.misc.items():
            k = codecs.encode(k, ENCODING) if not isinstance(k, bytes) else k
            v = codecs.encode(v, ENCODING) if not isinstance(v, bytes) else v
            misc.append(b'#' + k + b' ' + v)

        lnObj = b''
        if self.ln_end_channel:
            # noinspection PyTypeChecker
            lnObj = b"#LNOBJ " + (codecs.encode(self.ln_end_channel, ENCODING)
                if not isinstance(self.ln_end_channel, bytes) else self.ln_end_channel)

        assert len(self.bpms) < 35*36+35 ,\
            f"The writer doesn't support more than {35*36+35} BPMs, open up a new issue if this is needed."

        exbpms = []
        for e, b in enumerate(self.bpms, 1):
            exbpms.append(b'#BPM' + bytes(base_repr(e, 36).zfill(2), 'ascii') +
                          b' ' + bytes(f"{b.bpm:.3f}", 'ascii'))

        wavs = []
        for k, v in self.samples.items():
            k = codecs.encode(k, ENCODING) if not isinstance(k, bytes) else k
            v = codecs.encode(v, ENCODING) if not isinstance(v, bytes) else v
            wavs.append(b'#WAV' + k + b' ' + v)

        return b'\r\n'.join(
            [title, artist, bpm, playLevel, *misc, lnObj, *exbpms, *wavs]
        )

    def _read_notes(self, data: List[dict], config: dict):
        """ The data will be in the format [{measure, channel, seq}, ...]

        This function helps .read
        """

        Hit     = namedtuple('Hit',  ['sample', 'measure', 'beat', 'slot'])
        Hold    = namedtuple('Hold', ['hit', 'sample', 'measure', 'beat', 'slot'])

        bpm_changes_snap = [BpmChangeSnap(self.bpms[0].bpm, 0, 0, Fraction(0), DEFAULT_BEAT_PER_MEASURE)]
        hits  = [[] for _ in range(MAX_KEYS)]
        holds = [[] for _ in range(MAX_KEYS)]
        time_sig = {}

        def pair_(b_: bytes):
            for i_ in range(0, len(b_), 2):
                yield b_[i_:i_ + 2]

        for d in data:
            measure  = int(d['measure'])
            channel  = d['channel']
            sequence = d['sequence']

            if channel == BMSChannel.TIME_SIG:
                # Time Signatures always appear before BPM Changes
                beats_per_measure = float(sequence) * DEFAULT_BEAT_PER_MEASURE
                time_sig[measure] = beats_per_measure
            else:
                division = int(len(sequence) / 2)

                # If the latest BPM is of the same measure,
                # this indicates that a TIME_SIG happened on the same measure
                # We will force the current measure to use the changed time sig.
                beats_per_measure = time_sig.get(measure, DEFAULT_BEAT_PER_MEASURE)
                for i, pair in enumerate(pair_(sequence)):
                    if pair == b'00': continue

                    beat = Fraction(i, division) * beats_per_measure
                    slot = beat % 1
                    beat = beat // 1
                    if channel == BMSChannel.BPM_CHANGE:
                        new_bpm = int(pair, 16)
                        bpm_changes_snap.append(
                            BpmChangeSnap(bpm=new_bpm, measure=measure, beat=beat,
                                          slot=slot, beats_per_measure=beats_per_measure)
                        )
                    elif channel == BMSChannel.EXBPM_CHANGE:
                        new_bpm = int(self.exbpms[pair])
                        bpm_changes_snap.append(
                            BpmChangeSnap(bpm=new_bpm, measure=measure, beat=beat,
                                          slot=slot, beats_per_measure=beats_per_measure)
                        )

                    elif channel in config.keys():
                        # Note
                        column = int(config[channel])

                        if pair == self.ln_end_channel:
                            # We found a matching tag for LNOBJ
                            try:
                                prev_hit = hits[column].pop(-1)
                                holds[column].append(
                                    Hold(hit=prev_hit, sample=prev_hit.sample, measure=measure, beat=beat, slot=slot)
                                )
                            except IndexError:
                                raise Exception(f"Previous Hit Not found for corresponding LN Tail on column {column}.")
                        else:
                            # Else it's a note
                            sample = self.samples.get(pair, None)
                            hits[column].append(Hit(sample=sample, measure=measure, beat=beat, slot=slot))

        if len(bpm_changes_snap) > 1 and \
           bpm_changes_snap[1].measure == 0 and \
           bpm_changes_snap[1].beat == 0 and \
           bpm_changes_snap[1].slot == 0:
            # This is a special case, where a BPM Change is on Measure 0, Beat 0, overriding the global BPM instantly
            # This shouldn't really happen but we patch it here.
            self.bpms.pop(0)
            bpm_changes_snap.pop(0)

        tm = TimingMap.time_by_snap(initial_offset=0,
                                    bpm_changes_snap=bpm_changes_snap)
        # Hits
        for col in range(MAX_KEYS):
            if not hits[col]: continue

            h: Hit
            measures, beats, slots = tuple(zip(*[[h.measure, h.beat, h.slot] for h in hits[col]]))

            # noinspection PyTypeChecker
            offsets = tm.offsets(measures=measures, beats=beats, slots=slots)
            for h, offset in zip(hits[col], offsets):
                self.notes.hits().append(BMSHit(h.sample, offset, col))

        # Holds
        for col in range(MAX_KEYS):
            if not holds[col]: continue

            h: Hold
            # noinspection PyUnresolvedReferences
            head_measures, head_beats, head_slots, tail_measures, tail_beats, tail_slots =\
                tuple(zip(*[[h.hit.measure, h.hit.beat, h.hit.slot, h.measure, h.beat, h.slot] for h in holds[col]]))

            # noinspection PyTypeChecker
            head_offsets = tm.offsets(measures=head_measures, beats=head_beats, slots=head_slots)
            tail_offsets = tm.offsets(measures=tail_measures, beats=tail_beats, slots=tail_slots)
            for h, head_offset, tail_offset in zip(holds[col], head_offsets, tail_offsets):
                self.notes.holds().append(BMSHold(h.sample, head_offset, col, _length=tail_offset - head_offset))

        # tm._force_bpm_measure()
        for b in tm.bpm_changes:
            # noinspection PyTypeChecker
            self.bpms.append(BMSBpm(offset=b.offset, bpm=b.bpm, metronome=b.beats_per_measure))

    def _write_notes(self,
                     note_channel_config: dict,
                     no_sample_default: bytes = b'01'):
        """ Writes the notes according to self data

        :param note_channel_config: The config from BMSChannel
        :param no_sample_default: The default byte to use when there's no sample
        :return:
        """

        tm = TimingMap.time_by_offset(0, [
            BpmChangeOffset(bpm=b.bpm, beats_per_measure=b.metronome, offset=b.offset) for b in self.bpms])
        sample_inv = {v: k for k, v in self.samples.items()}
        channel = note_channel_config

        metronome_changes = [b for b in self.bpms if b.metronome != 4]

        """ Find the objects we want to snap here """

        df = tm.snap_objects(
            [
                *self.notes.hits().offsets(),           # Hit Objects
                *self.notes.holds().offsets(),          # Head Objects
                *self.notes.holds().tail_offsets(),      # Tail Objects
                *self.bpms.offsets(),                   # BPM Changes
                *[m.offset for m in metronome_changes]  # Metronome Changes
            ],
            [
                # Hit Objects
                *[(sample_inv.get(h.sample, no_sample_default), h.column) for h in self.notes.hits()],
                # Head Objects
                *[(sample_inv.get(h.sample, no_sample_default), h.column) for h in self.notes.holds()],
                # Tail Objects
                *[(self.ln_end_channel, h.column) for h in self.notes.holds()],
                # EXBPM uses indexing the BPM from the header, which is neater. It starts from 01 - ZZ
                # BPM Changes
                *[(bytes(base_repr(e+1, 36).zfill(2), 'ascii'), "EXBPM_CHANGE") for e in range(len(self.bpms))],
                # Metronome Changes
                *[(bytes(f"{float(m.metronome):.4f}", 'ascii'), "TIME_SIG") for m in metronome_changes]
             ])

        """ Since the objects there are in tuples, we just loop and index """

        df['sample'] = [o[0] for o in df.obj]

        channel_map = {v: k for k, v in channel.items()}
        df['channel'] = [channel_map[o[1]] for o in df.obj]
        df.drop('obj', axis=1, inplace=True)

        """ We make the time signatures to be on beat so that it's render is simply the float.
         
         This works because seq = b['00'] is replaced with seq = b['sig'] and renders as 'sig'
         """

        # Time signatures must be on a beat
        df.loc[df.channel == channel_map['TIME_SIG'], 'beat'] = 0
        df.loc[df.channel == channel_map['TIME_SIG'], 'slot'] = 0

        """ Here, we find the beats per measure associated for each measure """
        measures = df.measure.max()
        ar = np.zeros([int(measures), 2])
        ar[:, 0] = np.arange(measures)

        # We are only interested in the beats per measure in BMS
        bpm_ar = np.asarray([(b.measure, b.beats_per_measure) for b in tm.bpm_changes])
        # Create a subtraction matrix
        a = np.arange(measures)[..., np.newaxis] - bpm_ar[:, 0]
        # Exclude any that are "before"
        a = np.where(a < 0, np.nan, a)
        # Find minimum matching
        b = np.nanargmin(a, axis=1)
        # Vectorize indexing
        ar[:, 1] = bpm_ar[b][:, 1]

        df_timing = pd.DataFrame(ar, columns=['measure', 'beats_per_measure'])
        df = pd.merge(df, df_timing, on=['measure'])

        """ Here, we calculate the expected position of the objects. 
        
        Note that time_sigs don't have position, we circumvented this by making the beat and slot 0. """

        # Get expected relative position [0,1]
        df['position'] = (df.slot + df.beat) / df.beats_per_measure

        # Slot to possible slots
        s = TimingMap.Slotter()
        df['position'] = [s.slot(i) for i in df.position]
        df['position_den'] = [i.denominator for i in df.position]

        # We then use a modified LCM. The difference is that the denominator is limited
        df_lcm = df[['measure', 'channel', 'position_den']].groupby(['measure', 'channel'], as_index=False)
        for ix, df_ in df_lcm:
            # noinspection PyProtectedMember
            a = TimingMap._reduce_exact_limit(list(df_.position_den), 100)
            mask = (df.measure == ix[0]) & (df.channel == ix[1])
            df.loc[mask, 'position_den'] = a
        df.position *= df.position_den

        """ Write out here. """

        # Generate the lines here
        df_out = df[['measure', 'channel', 'position_den', 'position', 'sample']].groupby(
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

    def data(self) -> Dict[str, TimedList]:
        """ Gets the notes, bpms as a dictionary """
        return {'notes': self.notes,
                'bpms': self.bpms}

    # noinspection PyMethodOverriding
    def metadata(self) -> str:
        """ Grabs the map metadata

        :return:
        """

        def formatting(artist, title, difficulty):
            return f"{artist} - {title}, {difficulty})"

        return formatting(self.artist, self.title, self.version)

    def rate(self, by: float, inplace:bool = False):
        """ Changes the rate of the map

        :param by: The value to rate it by. 1.1x speeds up the song by 10%. Hence 10/11 of the length.
        :param inplace: Whether to perform the operation in place. Returns a copy if False
        """
        this = self if inplace else self.deepcopy()
        super(BMSMap, this).rate(by=by, inplace=True)

        return None if inplace else this

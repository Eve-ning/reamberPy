from __future__ import annotations

import codecs
import logging
import warnings
from collections import namedtuple
from dataclasses import dataclass, field
from fractions import Fraction
from typing import List, Dict

import numpy as np
import pandas as pd
from numpy import base_repr

from reamber.algorithms.timing import TimingMap
from reamber.algorithms.timing.utils import BpmChangeSnap, BpmChangeOffset, \
    find_lcm
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

DEFAULT_BEAT_PER_MEASURE = 4
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
                    log.debug(
                        f"Added {line_split[0][1:]}: {line_split[1]} header entry")
                    # [1:] Remove the #
                    header[line_split[0][1:]] = line_split[1]

                elif len(line_split) == 1:
                    if ord('0') <= line_split[0][1] <= ord(
                        '9'):  # ASCII for numbers
                        # Is note
                        command, data = line_split[0].split(b':')
                        measure = command[1:4]
                        channel = command[4:6]
                        sequence = data

                        log.debug(
                            f"Added {measure}, {channel}, {sequence} note entry")
                        notes.append(dict(measure=measure, channel=channel,
                                          sequence=sequence))
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
    def read_file(file_path: str,
                  note_channel_config: dict = BMSChannel.BME) -> BMSMap:
        """ Reads the file, depending on the config, keys may change

        If unsure, use the default BME. If all channels don't work please report an issue with it with the file

        The Channel config determines which channel goes to which keys, that means using the wrong channel config
        may scramble the notes.

        :param file_path: Path to file
        :param note_channel_config: Get this config from reamber.bms.BMSChannel
        :return:
        """
        with codecs.open(file_path, mode="r", encoding=ENCODING) as f:
            lines = [line.strip() for line in f.readlines()]

        return BMSMap.read(lines, note_channel_config=note_channel_config)

    def _reparse_bpm(self):
        """ Because when we read the BMS file, sometimes the bpms aren't fitted properly, thus, we need to
        premptively reparse it by snapping to offset and back to snaps again.

        During _write_notes, if the time_by_offset tm isn't reparsed, corrective bpm lines will not generate.
        """
        tm = TimingMap.time_by_offset(0, [
            BpmChangeOffset(bpm=b.bpm, metronome=b.metronome,
                            offset=b.offset) for b in self.bpms])

        self.bpms = BMSBpmList(
            [BMSBpm(b.offset, b.bpm, b.beats_per_measure) for b in
             tm.bpm_changes])

    def write(self,
              note_channel_config: dict = BMSChannel.BME,
              no_sample_default: bytes = b'01'):
        self._reparse_bpm()
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

        :param file_path: Path to write to
        :param note_channel_config: The config from BMSChannel
        :param no_sample_default: The default byte to use when there's no sample
        :return:
        """
        with open(file_path, "wb+") as f:
            f.write(self.write(note_channel_config=note_channel_config,
                               no_sample_default=no_sample_default))

    def _read_file_header(self, data: dict):
        self.artist = data.pop(b'ARTIST') if b'ARTIST' in data.keys() else ""
        self.title = data.pop(b'TITLE') if b'TITLE' in data.keys() else ""
        self.version = data.pop(
            b'PLAYLEVEL') if b'PLAYLEVEL' in data.keys() else ""
        self.ln_end_channel = data.pop(
            b'LNOBJ') if b'LNOBJ' in data.keys() else b''

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

        # We do this to go in-line with the temporary measure property assigned in _readNotes.
        bpm = BMSBpm(0, bpm=float(data.pop(b'BPM')))

        log.debug(f"Added initial BPM {bpm.bpm}")
        self.bpms = self.bpms.append(bpm)

        self.misc = data

    def _write_file_header(self) -> bytes:
        # May need to change all header stuff to a byte string first.

        # noinspection PyTypeChecker
        title = b"#TITLE " + (codecs.encode(self.title, ENCODING)
                              if not isinstance(self.title,
                                                bytes) else self.title)

        # noinspection PyTypeChecker
        artist = b"#ARTIST " + (codecs.encode(self.artist, ENCODING)
                                if not isinstance(self.artist,
                                                  bytes) else self.artist)

        bpm = b"#BPM " + codecs.encode(str(self.bpms[0].bpm), ENCODING)

        # noinspection PyTypeChecker
        play_level = b"#PLAYLEVEL " + (codecs.encode(self.version)
                                       if not isinstance(self.version,
                                                         bytes) else self.version)
        misc = []
        for k, v in self.misc.items():
            k = codecs.encode(k, ENCODING) if not isinstance(k, bytes) else k
            v = codecs.encode(v, ENCODING) if not isinstance(v, bytes) else v
            misc.append(b'#' + k + b' ' + v)

        ln_obj = b''
        if self.ln_end_channel:
            # noinspection PyTypeChecker
            ln_obj = b"#LNOBJ " + (codecs.encode(self.ln_end_channel, ENCODING)
                                   if not isinstance(self.ln_end_channel,
                                                     bytes) else self.ln_end_channel)

        assert len(self.bpms) < 35 * 36 + 35, \
            f"The writer doesn't support more than {35 * 36 + 35} BPMs, open up a new issue if this is needed."

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
            [title, artist, bpm, play_level, *misc, ln_obj, *exbpms, *wavs]
        )

    def _read_notes(self, data: List[dict], config: dict):
        """ The data will be in the format [{measure, channel, seq}, ...]

        This function helps .read
        """

        Hit = namedtuple('Hit', ['sample', 'measure', 'beat', 'slot'])
        Hold = namedtuple('Hold', ['hit', 'sample', 'measure', 'beat', 'slot'])

        bpm_changes_snap = [BpmChangeSnap(self.bpms[0].bpm, 0, 0, Fraction(0),
                                          DEFAULT_BEAT_PER_MEASURE)]
        hits = [[] for _ in range(MAX_KEYS)]
        holds = [[] for _ in range(MAX_KEYS)]
        time_sig = {}

        def pair_(b_: bytes):
            for i_ in range(0, len(b_), 2):
                yield b_[i_:i_ + 2]

        # One issue is that the time_sig channel call does not sustain for more than 1 measure.
        # Hence, if the time_sig changes, it's only for that measure.
        # Thus, if the time_sig changes, it'll require correction for the next measure if needed.

        for d in data:
            measure = int(d['measure'])
            channel = d['channel']
            sequence = d['sequence']

            if channel == BMSChannel.TIME_SIG:
                # Time Signatures always appear before BPM Changes
                metronome = float(sequence) * DEFAULT_BEAT_PER_MEASURE
                time_sig[measure] = metronome
                bpm_changes_snap.append(
                    BpmChangeSnap(bpm=self.bpms[-1].bpm, measure=measure,
                                  beat=0, snap=0,
                                  metronome=metronome)
                )
            else:
                division = int(len(sequence) / 2)

                # If the latest BPM is of the same measure,
                # this indicates that a TIME_SIG happened on the same measure
                # We will force the current measure to use the changed time sig.
                metronome = time_sig.get(measure, DEFAULT_BEAT_PER_MEASURE)
                for i, pair in enumerate(pair_(sequence)):
                    if pair == b'00' or pair == b'0': continue

                    beat = Fraction(i, division) * metronome
                    snap = beat % 1
                    beat = beat // 1
                    if channel == BMSChannel.BPM_CHANGE or channel == BMSChannel.EXBPM_CHANGE:
                        new_bpm = int(pair,
                                      16) if channel == BMSChannel.BPM_CHANGE else float(
                            self.exbpms[pair])
                        prev = bpm_changes_snap[-1]
                        if prev.measure == measure and prev.beat + prev.snap - beat - snap < MERGE_DELTA:
                            prev.bpm = new_bpm
                        else:
                            bpm_changes_snap.append(
                                BpmChangeSnap(bpm=new_bpm, measure=measure,
                                              beat=beat,
                                              snap=snap, metronome=metronome)
                            )
                    elif channel in config.keys():
                        # Note
                        column = int(config[channel])

                        if pair == self.ln_end_channel:
                            # We found a matching tag for LNOBJ
                            try:
                                prev_hit = hits[column].pop(-1)
                                holds[column].append(
                                    Hold(hit=prev_hit, sample=prev_hit.sample,
                                         measure=measure, beat=beat, snap=snap)
                                )
                            except IndexError:
                                raise Exception(
                                    f"Previous Hit Not found for corresponding LN Tail on column {column}.")
                        else:
                            # Else it's a note
                            sample = self.samples.get(pair, None)
                            hits[column].append(
                                Hit(sample=sample, measure=measure, beat=beat,
                                    snap=snap))

        if len(bpm_changes_snap) > 1 and \
            bpm_changes_snap[1].measure == 0 and \
            bpm_changes_snap[1].beat == 0 and \
            bpm_changes_snap[1].snap == 0:
            # This is a special case, where a BPM Change is on Measure 0, Beat 0, overriding the global BPM instantly
            # This shouldn't really happen but we patch it here.
            self.bpms = self.bpms[1:]
            bpm_changes_snap.pop(0)

        """ Here we have to correct the lack of default metronome resets. 
        
        The problem is that BMS' time sig changes are only for the current measure, on the contrary, we assume it 
        carries forward to the next measures.
        
        The algorithm goes through all changes and adds an additional time sig change if the previous is non-normal
        and the current is lacking a reset.
        """

        bpm_changes_snap.sort(key=lambda x: (x.measure, x.beat, x.snap))
        for a, b in zip(bpm_changes_snap[:-1], bpm_changes_snap[1:]):
            # If b is at least a measure ahead
            if b.measure > a.measure:
                # If b is not on a measure
                if (b.beat != 0 and b.snap != 0) or b.measure - a.measure > 1:
                    bpm_changes_snap.append(
                        BpmChangeSnap(bpm=a.bpm, measure=a.measure + 1, beat=0,
                                      snap=0,
                                      metronome=DEFAULT_BEAT_PER_MEASURE))
        tm = TimingMap.time_by_snap(initial_offset=0,
                                    bpm_changes_snap=bpm_changes_snap)
        # Hits
        hit_list = []

        for col in range(MAX_KEYS):
            if not hits[col]: continue

            h: Hit
            measures, beats, slots = tuple(
                zip(*[[h.measure, h.beat, h.slot] for h in hits[col]]))

            # noinspection PyTypeChecker
            offsets = tm.offsets(measures=measures, beats=beats, slots=slots)
            hit_list.extend([BMSHit(sample=h.sample, offset=offset, column=col)
                             for h, offset in zip(hits[col], offsets)])
        self.hits = BMSHitList(hit_list)

        # Holds
        hold_list = []

        for col in range(MAX_KEYS):
            if not holds[col]: continue

            h: Hold
            # noinspection PyUnresolvedReferences
            head_measures, head_beats, head_slots, tail_measures, tail_beats, tail_slots = \
                tuple(zip(*[
                    [h.hit.measure, h.hit.beat, h.hit.snap, h.measure, h.beat,
                     h.slot] for h in holds[col]]))

            # noinspection PyTypeChecker
            head_offsets = tm.offsets(measures=head_measures, beats=head_beats,
                                      slots=head_slots)
            tail_offsets = tm.offsets(measures=tail_measures, beats=tail_beats,
                                      slots=tail_slots)
            hold_list.extend(
                [BMSHold(sample=h.sample, offset=head_offset, column=col,
                         length=tail_offset - head_offset)
                 for h, head_offset, tail_offset in
                 zip(holds[col], head_offsets, tail_offsets)]
            )

        self.holds = BMSHoldList(hold_list)

        # tm._force_bpm_measure()
        self.bpms = BMSBpmList(
            [BMSBpm(offset=b.offset, bpm=b.bpm, metronome=b.beats_per_measure)
             for b in tm.bpm_changes])

    def _write_notes(self,
                     note_channel_config: dict,
                     no_sample_default: bytes = b'01'):

        """ Writes the notes according to self data

        :param note_channel_config: The config from BMSChannel
        :param no_sample_default: The default byte to use when there's no sample
        :return:
        """
        warnings.warn("Maps with many BPM Changes will likely break this. "
                      "Open up an Issue to support this fully.")
        tm = TimingMap.time_by_offset(0, [
            BpmChangeOffset(bpm=b.bpm, metronome=b.metronome,
                            offset=b.offset) for b in self.bpms])
        sample_inv = {v: k for k, v in self.samples.items()}
        channel = note_channel_config

        metronome_changes = [b for b in self.bpms if b.metronome != 4]

        """ Find the objects we want to snap here """

        df = tm.snap_objects(
            [
                *self.hits.offset,
                *self.holds.offset,
                *self.holds.tail_offset,
                *self.bpms.offset,  # BPM Changes
                *[m.offset for m in metronome_changes]  # Metronome Changes
            ],
            [
                # Hit Objects
                *[(sample_inv.get(h.sample, no_sample_default), h.column) for h
                  in self.hits],
                # Head Objects
                *[(sample_inv.get(h.sample, no_sample_default), h.column) for h
                  in self.holds],
                # Tail Objects
                *[(self.ln_end_channel, h.column) for h in self.holds],
                # EXBPM uses indexing the BPM from the header, which is neater. It starts from 01 - ZZ
                # BPM Changes
                *[(bytes(base_repr(e + 1, 36).zfill(2), 'ascii'),
                   "EXBPM_CHANGE") for e in range(len(self.bpms))],
                # Metronome Changes
                *[(
                  bytes(f"{float(m.metronome) / DEFAULT_BEAT_PER_MEASURE:.4f}",
                        'ascii'), "TIME_SIG") for m in metronome_changes]
            ])

        """ Since the objects there are in tuples, we just loop and index """

        df['sample'] = [o[0] for o in df.obj]

        channel_map = {v: k for k, v in channel.items()}
        df['channel'] = [channel_map[o[1]] for o in df.obj]
        df = df.drop('obj', axis=1)

        """ We make the time signatures to be on beat so that it's render is simply the float.
         
        This works because seq = b['00'] is replaced with seq = b['sig'] and renders as 'sig'
        """

        # Time signatures must be on a beat
        df.loc[df.channel == channel_map['TIME_SIG'], 'beat'] = 0
        df.loc[df.channel == channel_map['TIME_SIG'], 'slot'] = 0

        """ Here, we find the beats per measure associated for each measure
        
        This algorithm takes the BPM Metronomes and maps to a integer space: 0, 1, 2, ..., n        
        Note that all BPMs WILL BE ON MEASURES, this is because we reparsed the BPM, which adds corrections to make 
        all on measures.
        
        Then, this will forward fill (FF) the Metronomes.
        
        E.g.
        
        MEASURE  0  1  2  3  4  5
        METRON   4  -  3  -  4  5
        FFMETRON 4  4  3  3  4  5 ...
        
        With this, we can allocate all notes their respective Metronome (important for writing).
        
        """
        # We are only interested in the beats per measure in BMS
        measure_ar = np.asarray([b.measure for b in tm.bpm_changes])
        beats_ar = np.asarray([b.beats_per_measure for b in tm.bpm_changes])
        measure_mapping_ar = np.empty([int(np.max(df.measure) + 1)])
        measure_mapping_ar[:] = np.nan
        measure_mapping_ar[measure_ar] = beats_ar
        measure_mapping_df = pd.DataFrame(
            measure_mapping_ar).ffill().reset_index()
        measure_mapping_df.columns = ['measure', 'beats_per_measure']
        df = pd.merge(df, measure_mapping_df, on=['measure'])

        """ Here, we calculate the expected position of the objects. 
        
        Note that time_sigs don't have position, we circumvented this by making the beat and slot 0. """

        # Get expected relative position [0,1]
        df['position'] = (df.slot + df.beat) / df.beats_per_measure

        # Slot to possible slots
        s = TimingMap.Slotter()
        df['position'] = [s.snap(i) for i in df.position]
        df['position_den'] = [i.denominator for i in df.position]

        """ This step here reduces the denominator such that it's as compact as possible.
        
        E.g.
        
        MEASURE 0: Note on 3/4, Note on 3/8.
        This algorithm will detect that this is reducable to 6/8 and 3/8, this makes it compact when writing out. 
        
        E.g.
        
        MEASURE 0: Note on 3/4, Note on 5/6.
        This algorithm will try to reduce to a limit of 100. That means, if we can represent both in the same line,
        with a character limit of 100, then we will.
        In this case, it can reduce to 9/12, 10/12. 12 < 100, so this is a reducable. 
        
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
    def metadata(self) -> str:
        """ Grabs the map metadata """

        def formatting(artist, title, difficulty):
            return f"{artist} - {title}, {difficulty})"

        return formatting(self.artist, self.title, self.version)

    @stack_props()
    class Stacker(Map.Stacker):
        _props = ["sample"]

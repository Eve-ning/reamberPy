from __future__ import annotations

import codecs
import logging
from collections import namedtuple
from dataclasses import dataclass, field
from fractions import Fraction
from math import ceil
from typing import List, Dict

import numpy as np

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
    def read(lines: List[str], noteChannelConfig: dict = BMSChannel.BME) -> BMSMap:
        """ Reads from a list of strings, depending on the config, keys may change

        If unsure, use the default BME. If all channels don't work please report an issue with it with the file

        The Channel config determines which channel goes to which keys, that means using the wrong channel config
        may scramble the notes.

        :param lines: List of strings from the file
        :param noteChannelConfig: Get this config from reamber.bms.BMSChannel
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

        bms._readFileHeader(header)
        bms._readNotes(notes, noteChannelConfig)

        return bms

    @staticmethod
    def readFile(filePath: str, noteChannelConfig: dict = BMSChannel.BME) -> BMSMap:
        """ Reads the file, depending on the config, keys may change

        If unsure, use the default BME. If all channels don't work please report an issue with it with the file

        The Channel config determines which channel goes to which keys, that means using the wrong channel config
        may scramble the notes.

        :param filePath: Path to file
        :param noteChannelConfig: Get this config from reamber.bms.BMSChannel
        :return:
        """
        with codecs.open(filePath, mode="r", encoding=ENCODING) as f:
            lines = [line.strip() for line in f.readlines()]

        return BMSMap.read(lines, noteChannelConfig=noteChannelConfig)

    def writeFile(self, filePath,
                  noteChannelConfig: dict = BMSChannel.BME,
                  snapPrecision: int = 96,
                  noSampleDefault: bytes = b'01',
                  maxSnapping: int = 384,
                  maxDenominator: int = 1000):
        """ Writes the notes according to self data

        :param filePath: Path to write to
        :param noteChannelConfig: The config from BMSChannel
        :param snapPrecision: The precision to snap all notes to
        :param noSampleDefault: The default byte to use when there's no sample
        :param maxSnapping: The maximum snapping
        :param maxDenominator: The maximum denominator to use in Fraction
        :return:
        """
        with open(filePath, "wb+") as f:
            f.write(self._writeFileHeader())
            f.write(b'\r\n' * 2)
            f.write(self._writeNotes(noteChannelConfig,
                                     snapPrecision=snapPrecision,
                                     noSampleDefault=noSampleDefault,
                                     maxDenominator=maxDenominator,
                                     maxSnapping=maxSnapping))

    def _readFileHeader(self, data: dict):
        self.artist         = data.pop(b'ARTIST')     if b'ARTIST'    in data.keys() else ""
        self.title          = data.pop(b'TITLE')      if b'TITLE'     in data.keys() else ""
        self.version        = data.pop(b'PLAYLEVEL')  if b'PLAYLEVEL' in data.keys() else ""
        self.ln_end_channel = data.pop(b'LNOBJ')      if b'LNOBJ'     in data.keys() else b''

        # We cannot pop during a loop, so we save the keys then pop later.
        toPop = []
        for k, v in data.items():
            if k[:3] == b'WAV':
                self.samples[k[-2:]] = v
                toPop.append(k)

        for k in toPop:
            data.pop(k)

        # We do this to go in-line with the temporary measure property assigned in _readNotes.
        bpm = BMSBpm(0, bpm=float(data.pop(b'BPM')))
        bpm.measure = 0

        log.debug(f"Added initial BPM {bpm.bpm}")
        self.bpms.append(bpm)

        self.misc = data

    def _writeFileHeader(self) -> bytes:
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

        wavs = []
        for k, v in self.samples.items():
            k = codecs.encode(k, ENCODING) if not isinstance(k, bytes) else k
            v = codecs.encode(v, ENCODING) if not isinstance(v, bytes) else v
            wavs.append(b'#WAV' + k + b' ' + v)

        return b'\r\n'.join(
            [title, artist, bpm, playLevel, *misc, lnObj, *wavs]
        )

    def _readNotes(self, data: List[dict], config: dict):
        """

        The data will be in the format [{measure, channel, seq}, ...]
        :param data:
        :param config:
        :return:
        """

        Hit     = namedtuple('Hit',     ['sample', 'measure', 'beat', 'slot'])
        Hold    = namedtuple('Hold',    ['hit', 'sample', 'measure', 'beat', 'slot'])

        bpm_changes_snap = [BpmChangeSnap(self.bpms[0].bpm, 0, 0, Fraction(0), DEFAULT_BEAT_PER_MEASURE)]
        hits  = [[] for _ in range(MAX_KEYS)]
        holds = [[] for _ in range(MAX_KEYS)]
        time_sig = {}

        def pair_(b: bytes):
            for i in range(0, len(b), 2):
                yield b[i:i+2]

        for d in data:
            measure  = int(d['measure'])
            channel  = d['channel']
            sequence = d['sequence']

            if channel == BMSChannel.TIME_SIG:
                # Time Signatures always appear before BPM Changes
                beats_per_measure = float(sequence) * DEFAULT_BEAT_PER_MEASURE
                time_sig[measure] = beats_per_measure
                # bpm_changes_snap.append(
                #     BpmChangeSnap(bpm=bpm_changes_snap[-1].bpm, measure=measure, beat=0,
                #     slot=Fraction(0), beats_per_measure=beats_per_measure)
                # )
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

        if bpm_changes_snap[1].measure == 0 and \
           bpm_changes_snap[1].beat == 0 and \
           bpm_changes_snap[1].slot == 0:
            # This is a special case, where a BPM Change is on Measure 0, Beat 0, overriding the global BPM instantly
            # This shouldn't really happen but we patch it here.
            self.bpms.pop(0)
            bpm_changes_snap.pop(0)

        tm = TimingMap.time_by_snap(initial_offset=0,
                                    bpm_changes_snap=bpm_changes_snap)
        np.diff(tm.offsets([35, 36, 36], [3, 0, 1], [0, 0, 0]))
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

        tm._force_bpm_measure()
        for b in tm.bpm_changes:
            self.bpms.append(BMSBpm(offset=b.offset, bpm=b.bpm, metronome=b.beats_per_measure))


    def _writeNotes(self,
                    noteChannelConfig: dict,
                    noSampleDefault: bytes = b'01',
                    snapPrecision: int = 96,
                    maxSnapping: int = 384,
                    maxDenominator: int = 1000):
        """ Writes the notes according to self data

        :param noteChannelConfig: The config from BMSChannel
        :param snapPrecision: The precision to snap all notes to
        :param noSampleDefault: The default byte to use when there's no sample
        :param maxSnapping: The maximum snapping
        :param maxDenominator: The maximum denominator to use in Fraction
        :return:
        """

        tm = TimingMap.time_by_offset(0, [BpmChangeOffset(bpm=b.bpm, beats_per_measure=DEFAULT_BEAT_PER_MEASURE,
                                                          offset=b.offset) for b in self.bpms])
        snaps      = tm.snaps(self.notes.hits().offsets())
        head_snaps = tm.snaps(self.notes.holds().headOffsets())
        tail_snaps = tm.snaps(self.notes.holds().tailOffsets())



        bpmMeasures = [b / 4 for b in BMSBpm.getBeats(self.bpms.offsets(), self.bpms)]
        prevMeasure = None
        for measure, bpm in zip(bpmMeasures[1:], self.bpms[1:]):
            if round(measure) == prevMeasure:
                log.debug(f"Bpm Dropped {bpm} due to overlapping integer.")
                continue
            out.append(b"#"
                       + bytes(f"{round(measure):03d}", encoding='ascii')
                       + b'03:'
                       + bytes(hex(round(bpm.bpm)), encoding='ascii')[2:])
            prevMeasure = round(measure)

        return b"\r\n".join(out)

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

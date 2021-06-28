from __future__ import annotations

import codecs
import logging
from dataclasses import dataclass, field
from fractions import Fraction
from math import ceil
from typing import List, Dict

import numpy as np

from reamber.base.Map import Map
from reamber.base.RAConst import RAConst
from reamber.base.lists.TimedList import TimedList
from reamber.bms.BMSBpm import BMSBpm
from reamber.bms.BMSChannel import BMSChannel
from reamber.bms.BMSHit import BMSHit
from reamber.bms.BMSHold import BMSHold
from reamber.bms.BMSMapMeta import BMSMapMeta
from reamber.bms.lists.BMSBpmList import BMSBpmList
from reamber.bms.lists.BMSNotePkg import BMSNotePkg
from reamber.timing import TimingMap

log = logging.getLogger(__name__)
ENCODING = "shift_jis"

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
                        sequence = [data[i:j+1] for i, j in zip(range(0, len(data), 2), range(1, len(data), 2))]

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

    @dataclass
    class _Hit:
        measure: float
        column: int
        sample: bytes

    @dataclass
    class _Hold:
        measure: float
        column: int
        tailMeasure: float
        sample: bytes

    @dataclass
    class _Bpm:
        measure: float
        bpm: int

    def _readNotes(self, data: List[dict], config: dict):

        # We assume 4 beats per measure. I know there's a metronome thing going on but it's hard to implement.
        # I will consider if there's high demand. Issue #25
        BEATS_PER_MEASURE = 4

        # The very first bpm is the one in the header, at 0th measure
        prev_bpm_measure = 0
        hit_measure_history = {}

        # Format: (Val, Measure, Beat, Divisor, Slot)
        bpms = []
        hits = [[] for _ in range(18)]  # 18 as it's the highest supported BMS col
        holds = [[] for _ in range(18)]

        @dataclass
        class Bpm:
            bpm: float
            measure: int
            beat: int
            divisor: int
            slot: int

        @dataclass
        class Hit:
            sample: bytes
            measure: int
            beat: int
            divisor: int
            slot: int

        @dataclass
        class Hold:
            head: Hit
            sample: bytes
            measure: int
            beat: int
            divisor: int
            slot: int

        # Here we read all the notes, bpm changes as measures, we'll post process them later.
        for measure_data in data:
            channel = measure_data['channel']
            measure = int(measure_data['measure'])
            seq     = measure_data['sequence']

            # This pads the sequence so that it's easier to read.
            if len(seq) == 1:
                seq = [seq[0], b'00', b'00', b'00']
            elif len(seq) == 2:
                seq = [seq[0], b'00', seq[1], b'00']

            if channel in config.keys():
                config_case = config[channel]

                if isinstance(config_case, (float, int)):
                    # If the Config is a Number, then it's a note. Else it's a BPM Change.
                    # See BMSChannel.py

                    column = int(config_case)
                    divisor = int(len(seq) / BEATS_PER_MEASURE)

                    # Note that the slot is relative to the measure instead of the beat!
                    for mslot, data in enumerate(seq):
                        if data == b'00': continue
                        slot = mslot % divisor
                        beat = mslot // divisor
                        # Will get None if doesn't exist. See Issue #20.
                        sample = self.samples.get(data, None)
                        if data != self.ln_end_channel:
                            hits[column].append(Hit(
                                sample=sample,
                                measure=measure,
                                beat=beat,
                                divisor=divisor,
                                slot=slot
                            ))

                            log.debug(f"Note at Col {column}, "
                                      f"Measure {measure}, "
                                      f"Beat {beat}, "
                                      f"Snap {slot} / {divisor}, "
                                      f"Sample {sample}")

                        else:  # This means we found an LN End, we have to look back to see which note is the head.
                            try:
                                hit_head = hit_measure_history[config_case]
                                holds[column].append(
                                    Hold(head=hits[column][-1],
                                         sample=hit_head.sample,
                                         measure=measure,
                                         beat=beat,
                                         divisor=divisor,
                                         slot=slot)
                                )

                                log.debug(f"LN Tail at Col {column}, "
                                          f"Measure {measure}, "
                                          f"Beat {beat}, "
                                          f"Snap {slot} / {divisor}, "
                                          f"Sample {sample}")

                            except KeyError:
                                raise Exception(f"Cannot find LN Head for Col {config_case}"
                                                f"Measure {measure}, "
                                                f"Beat {beat}, "
                                                f"Snap {slot} / {divisor}, "
                                                f"Sample {sample}")

                # This indicates the BPM Change
                elif config_case == 'BPM_CHANGE':
                    log.debug(f"Bpm Change,"
                              f"Measure {int(measure_data['measure'])},"
                              f"BPM {int(measure_data['sequence'][0], 16)}")

                    bpm = int(seq[0], 16)

                    measure = int(measure_data['measure'])
                    # BPM is in hex, int(x, 16) to convert hex to int
                    self.bpms.append(
                        BMSBpm(bpm=bpm,
                               offset=RAConst.minToMSec((measure - prev_bpm_measure) * BEATS_PER_MEASURE / self.bpms[-1].bpm) +
                                      self.bpms[-1].offset))

                    prev_bpm_measure = measure

                # elif keysounding config cases here!
                # Not supporting it because there's no demand yet

        """ Measure Processing
        
        We do the same algorithm as O2Jam where we extract all measures, hits, hold heads and hold tails.
        
        The reason we do this is because it's hard to loop hold head and hold tail separately without extracting them
        separately. So we get all possible unique measures, then map them to the measures originally.
        """

        # We will replace all item values as we loop through
        measures = dict(sorted({**{x.measure: 0 for x in hits},
                                **{x.measure: 0 for x in holds},
                                **{x.tailMeasure: 0 for x in holds}}.items()))

        """ Here we loop through all possible measures while going through bpms. """

        i = 0
        currBpm = self.bpms[i].bpm
        currBpmOffset = 0
        currBpmMeasure = 0

        if len(self.bpms) > i + 1:
            nextBpm = self.bpms[i + 1].bpm
            nextBpmOffset = self.bpms[i + 1].offset
            nextBpmMeasure = (nextBpmOffset - currBpmOffset) * RAConst.mSecToMin(currBpm) / BEATS_PER_MEASURE
        else:
            nextBpm = None
            nextBpmOffset = None
            nextBpmMeasure = None

        for measure in measures.keys():
            # We do while because there may be multiple bpms before the next hit is found.
            while nextBpmMeasure and measure >= nextBpmMeasure:

                log.debug(f"Changed Bpm from {currBpm} to {nextBpm} at"
                          f"Measure {measure} >= bpm measure {nextBpmMeasure}")
                currBpm = nextBpm
                currBpmMeasure = nextBpmMeasure
                currBpmOffset = nextBpmOffset

                i += 1

                if len(self.bpms) > i + 1:
                    nextBpm = self.bpms[i + 1].bpm
                    nextBpmOffset = self.bpms[i + 1].offset
                    nextBpmMeasure = (nextBpmOffset - currBpmOffset) * RAConst.mSecToMin(currBpm) / BEATS_PER_MEASURE +\
                                     currBpmMeasure
                else:
                    nextBpm = None
                    nextBpmOffset = None
                    nextBpmMeasure = None

            # Here, it's guaranteed that the currBpm is correct.
            offset = RAConst.minToMSec((measure - currBpmMeasure) * BEATS_PER_MEASURE / currBpm) + currBpmOffset
            measures[measure] = offset
            log.debug(f"Mapped measure {measure} to offset {offset}ms")

        for hit in hits:
            if not hasattr(hit, 'matched'):
                # We previously added a temp 'matched' attr when adding the hold heads to find out if we should add this
                self.notes.hits().append(BMSHit(offset=measures[hit.measure], column=hit.column, sample=hit.sample))

        for hold in holds:
            self.notes.holds().append(BMSHold(offset=measures[hold.measure], column=hold.column,
                                              _length=measures[hold.tailMeasure] - measures[hold.measure],
                                              sample=hold.sample))

        self.notes.hits().sorted(inplace=True)
        self.notes.holds().sorted(inplace=True)

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
        notes = [[hit.offset, hit.sample, hit.column] for hit in self.notes.hits()] + \
                [[hold.offset, hold.sample, hold.column] for hold in self.notes.holds()] + \
                [[hold.tailOffset(), self.ln_end_channel, hold.column] for hold in self.notes.holds()]

        notes.sort(key=lambda x: x[0])

        notesAr = np.empty((len(notes)), dtype=[('measure', float), ('column', np.int), ('sample', object)])

        # We snap exact because ms isn't always accurate. We'll snap to the nearest 1/192nd
        notesAr['measure'] = BMSBpm.snapExact([i[0] for i in notes], self.bpms, snapPrecision)
        notesAr['sample'] = [i[1] for i in notes]
        notesAr['column'] = [i[2] for i in notes]
        notesAr['measure'] = np.round(BMSBpm.getBeats(list(notesAr['measure']), self.bpms), 4) / 4
        lastMeasure = ceil(notesAr['measure'].max())
        measures = notesAr['measure']
        sampleDict = {v: k for k, v in self.samples.items() if v is not None}
        configDict = {v: k for k, v in noteChannelConfig.items()}
        if self.ln_end_channel: sampleDict[self.ln_end_channel] = self.ln_end_channel

        out = []
        for measureStart, measureEnd in zip(range(0, lastMeasure), range(1, lastMeasure + 1)):
            notesInMeasure = notesAr[(measureStart <= measures) & (measures < measureEnd)]
            if len(notesInMeasure) == 0: continue
            colsInMeasure = set(notesInMeasure['column'])

            for col in colsInMeasure:
                measureHeader = b'#'\
                                + bytes(f"{measureStart:03d}", encoding='ascii')\
                                + configDict[col]\
                                + b':'
                notesInCol = notesInMeasure[notesInMeasure['column'] == col]

                # We get rid of the 1s places and only get the decimal since we want its relative position.
                measuresInCol = notesInCol['measure'] % 1
                denoms = [Fraction(i).limit_denominator(maxDenominator).denominator for i in measuresInCol]

                """Approximation happens here
                
                What happens is that usually if we go from a ms based map to BMS, you'd get a super high LCM because
                of millisecond rounding. So what I do is that I approximate it to the closes 192nd snap by forcing
                the slots to be 192 max.
                
                LCM will break if the LCM is too large, causing an overflow to snaps < 0, that's why that condition.
                
                LCM gives 0 if any entry is 0, we want at least one.
                """

                try:
                    # noinspection PyUnresolvedReferences
                    snaps = np.lcm.reduce([i for i in denoms if i != 0])
                except TypeError:
                    snaps = 1
                if snaps > maxSnapping or snaps < 0:  # We might as well approximate as this point
                    snaps = maxSnapping
                elif snaps == 0:
                    snaps = 1

                slotsInCol = np.round(measuresInCol * snaps)
                measure = [b'0', b'0'] * snaps
                log.debug(f"Note Slotting: Measures: {measuresInCol}"
                          f"Col: {col}"
                          f"Slots: {slotsInCol}"
                          f"Snaps: {snaps}")

                for note, slot in zip(notesInCol, slotsInCol):

                    # If we cannot find the sample, then we default to noSampleDefault == b'01'
                    try:
                        sampleChannel = sampleDict[note['sample']]
                    except KeyError:
                        sampleChannel = noSampleDefault

                    measure[int(slot * 2)] = bytes(str(sampleChannel, 'ascii')[0], 'ascii')
                    measure[int(slot * 2 + 1)] = bytes(str(sampleChannel, 'ascii')[1], 'ascii')

                out.append(measureHeader + b''.join(measure))

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

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict
import numpy as np

from reamber.base.RAConst import RAConst
from reamber.base.Map import Map
from reamber.base.lists.TimedList import TimedList
from reamber.bms.BMSBpm import BMSBpm
from reamber.bms.BMSHit import BMSHit
from reamber.bms.BMSHold import BMSHold
from reamber.bms.BMSMapMeta import BMSMapMeta
from reamber.bms.lists.BMSBpmList import BMSBpmList
from reamber.bms.lists.BMSNotePkg import BMSNotePkg
from fractions import Fraction
from math import ceil

import codecs

import logging

log = logging.getLogger(__name__)
ENCODING = "shift_jis"
NO_SAMPLE_DEFAULT = b'01'

@dataclass
class BMSMap(Map, BMSMapMeta):

    notes: BMSNotePkg = field(default_factory=lambda: BMSNotePkg())
    bpms:  BMSBpmList = field(default_factory=lambda: BMSBpmList())

    @staticmethod
    def readFile(filePath, noteChannelConfig: dict) -> BMSMap:
        """

        :param filePath:
        :param noteChannelConfig: Get this config from reamber.bms.BMSChannel
        :return:
        """
        self = BMSMap()

        with codecs.open(filePath, mode="r", encoding=ENCODING) as f:

            line = f.readline()
            header = {}
            notes = []

            while line:
                # Check if it's a command
                if line[0] == '#':
                    # We split it by b' '.
                    # If it's size == 2, then it's a header metadata
                    # Else, it may be an unfilled header or a note data.

                    # Sometimes titles have spaces, so we split maximum of once.
                    line0 = line.encode('shift_jis').strip().split(b' ', 1)

                    if len(line0) == 2:
                        # Header Metadata (Filled)
                        log.debug(f"Added {line0[0][1:]}: {line0[1]} header entry")
                        header[line0[0][1:]] = line0[1]
                        # We don't support keysounding, we'll still parse it into a dictionary though.
                        # Refer to Issue#20.
                        # We feed these into metadata, [1:] because the command character is not needed.
                        # If we want to support keysounding, here's where the code will be inserted
                        """ Pseudo keysounding

                        if line0[0][1:4] == b'WAV' then
                            channel = line0[0][-2:]
                            file = line[1]
                            # feed these into the dictionary as a list.

                        So it can be accessed as:
                        e.g. metadata['WAV'][3] 
                        """

                    elif len(line0) == 1:
                        if 48 <= line0[0][1] <= 57:  # ASCII for numbers
                            # Is note
                            lineNote = line0[0].split(b':')
                            measure = lineNote[0][1:4]
                            channel = lineNote[0][4:6]
                            sequence = [lineNote[1][i:i + 2] for i in range(0, len(lineNote[1]), 2)]

                            log.debug(f"Added {measure}, {channel}, {sequence} note entry")
                            notes.append(dict(measure=measure, channel=channel, sequence=sequence))
                        else:
                            # Header Data (Unfilled) <Ignored>
                            pass
                    else:
                        # Unexpected data.
                        pass

                line = f.readline()
            self._readFileHeader(header)
            self._readNotes(notes, noteChannelConfig)
        return self

    def writeFile(self, filePath, noteChannelConfig: dict):
        with open(filePath, "wb+") as f:
            f.write(self._writeFileHeader())
            f.write(b'\r\n' * 2)
            f.write(self._writeNotes(noteChannelConfig))

    def _readFileHeader(self, data: dict):
        self.artist = data.pop(b'ARTIST') if b'ARTIST' in data.keys() else ""
        self.title = data.pop(b'TITLE') if b'TITLE' in data.keys() else ""
        self.version = data.pop(b'PLAYLEVEL') if b'PLAYLEVEL' in data.keys() else ""
        self.lnEndChannel = data.pop(b'LNOBJ') if b'LNOBJ' in data.keys() else b''

        # We cannot pop during a loop, so we save the keys then pop later.
        toPop = []
        for k, v in data.items():
            if k[:3] == b'WAV':
                self.samples[k[-2:]] = v
                toPop.append(k)

        for k in toPop:
            data.pop(k)

        # We do this to go in-line with the temporary measure property assigned in _readNotes.
        bpm = BMSBpm(0, bpm=int(data.pop(b'BPM')))
        bpm.measure = 0

        log.debug(f"Added initial BPM {bpm.bpm}")
        self.bpms.append(bpm)

        self.misc = data

    def _writeFileHeader(self) -> bytes:
        # May need to change all header stuff to a byte string first.

        title = b"#TITLE " + (codecs.encode(self.title, ENCODING)
                             if not isinstance(self.title, bytes) else self.title)

        artist = b"#ARTIST " + (codecs.encode(self.artist, ENCODING)
                               if not isinstance(self.artist, bytes) else self.artist)

        bpm = b"#BPM " + codecs.encode(self.bpms[0].bpm, ENCODING)

        playLevel = b"#PLAYLEVEL " + (codecs.encode(self.version)
                                     if not isinstance(self.version, bytes) else self.version)
        misc = []
        for k, v in self.misc.items():
            k = codecs.encode(k, ENCODING) if not isinstance(k, bytes) else k
            v = codecs.encode(v, ENCODING) if not isinstance(v, bytes) else v
            misc.append(b'#' + k + b' ' + v)

        lnObj = b''
        if self.lnEndChannel:
            # noinspection PyTypeChecker
            lnObj = b"#LNOBJ " + (codecs.encode(self.lnEndChannel, ENCODING)
                if not isinstance(self.lnEndChannel, bytes) else self.lnEndChannel)

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
        prevBpmMeasure = 0
        hits = []
        holds = []
        hitMeasureHistory = {}

        # Here we read all the notes, bpm changes as measures, we'll post process them later.
        for measureData in data:
            channel = measureData['channel']

            if channel in config.keys():
                configCase = config[channel]

                # If it's an int, float, it's a note, else it'd be a str, which indicates BPM Change, Metronome change,
                # etc.
                if isinstance(configCase, (float, int)):
                    seq = measureData['sequence']
                    seqI = np.where([i != b'00' for i in seq])[0]
                    length = len(measureData['sequence'])
                    for i in seqI:
                        if seq[i] != self.lnEndChannel:
                            hitMeasure = int(measureData['measure']) + i / length
                            hitSample = self.samples[measureData['sequence'][i]]
                            hit = BMSMap._Hit(column=configCase,
                                              measure=hitMeasure,
                                              sample=hitSample)
                            hits.append(hit)

                            log.debug(f"Note at Col {configCase}, Measure {hitMeasure}, sample")

                            hitMeasureHistory[configCase] = hit

                        else:  # This means we found an LN End, we have to look back to see which note is the head.
                            holdTMeasure = int(measureData['measure']) + i / length
                            try:
                                # HoldH is a Hit object.
                                holdH = hitMeasureHistory[configCase]
                                # noinspection PyCallByClass
                                holds.append(BMSMap._Hold(column=configCase,
                                                          measure=holdH.measure,
                                                          sample=holdH.sample,
                                                          tailMeasure=holdTMeasure))

                                # ! If we matched the head, we mark this hit as matched. See last few lines for how
                                # it is used.
                                holdH.matched = True

                                log.debug(f"LN Tail at Col {configCase}, Measure {holdTMeasure}")

                            except KeyError:
                                raise Exception(f"Cannot find LN Head for Col {configCase} at measure {holdTMeasure}")

                # This indicates the BPM Change
                elif configCase == 'BPM_CHANGE':
                    log.debug(f"Bpm Change,"
                              f"Measure {int(measureData['measure'])},"
                              f"BPM {int(measureData['sequence'][0], 16)}")

                    measure = int(measureData['measure'])
                    # BPM is in hex, int(x, 16) to convert hex to int
                    self.bpms.append(
                        BMSBpm(bpm=int(measureData['sequence'][0], 16),
                               offset=RAConst.minToMSec((measure - prevBpmMeasure) *
                                                        BEATS_PER_MEASURE / self.bpms[-1].bpm) +
                                      self.bpms[-1].offset))

                    prevBpmMeasure = measure

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

    def _writeNotes(self, noteChannelConfig: dict):

        notes = [[hit.offset, hit.sample, hit.column] for hit in self.notes.hits()] + \
                [[hold.offset, hold.sample, hold.column] for hold in self.notes.holds()] + \
                [[hold.tailOffset(), self.lnEndChannel, hold.column] for hold in self.notes.holds()]

        notes.sort(key=lambda x: x[0])

        notesAr = np.empty((len(notes)), dtype=[('measure', float), ('column', np.int), ('sample', object)])
        notesAr['measure'] = [i[0] for i in notes]
        notesAr['sample'] = [i[1] for i in notes]
        notesAr['column'] = [i[2] for i in notes]
        notesAr['measure'] = np.round(BMSBpm.getBeats(notesAr['measure'], self.bpms)[0], 6) / 4
        lastMeasure = ceil(notesAr['measure'].max())
        measures = notesAr['measure']
        sampleDict = {v: k for k, v in self.samples.items()}
        configDict = {v: k for k, v in noteChannelConfig.items()}
        if self.lnEndChannel: sampleDict[self.lnEndChannel] = self.lnEndChannel

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
                measuresInCol = notesInCol['measure'] % 1
                # noinspection PyUnresolvedReferences
                snaps = np.lcm.reduce([Fraction(i).limit_denominator(1000).denominator for i in measuresInCol])
                slotsInCol = np.round(measuresInCol * snaps)
                measure = [b'0', b'0'] * snaps
                for note, slot in zip(notesInCol, slotsInCol):

                    # If we cannot find the sample, then we default to NO_SAMPLE_DEFAULT == b'01'
                    try:
                        sampleChannel = sampleDict[note['sample']]
                    except KeyError:
                        sampleChannel = NO_SAMPLE_DEFAULT

                    measure[int(slot * 2)] = bytes(str(sampleChannel, 'ascii')[0], 'ascii')
                    measure[int(slot * 2 + 1)] = bytes(str(sampleChannel, 'ascii')[1], 'ascii')
                out.append(measureHeader + b''.join(measure))

        return b"\r\n".join(out)

    def data(self) -> Dict[str, TimedList]:
        """ Gets the notes, bpms as a dictionary """
        return {'notes': self.notes,
                'bpms': self.bpms}

    # noinspection PyMethodOverriding
    def metadata(self, unicode=True) -> str:
        """ Grabs the map metadata

        :param unicode: Whether to try to find the unicode or non-unicode. \
            This doesn't try to convert unicode to ascii, it just looks for if there's an available translation.
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

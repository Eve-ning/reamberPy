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

import codecs

import logging

log = logging.getLogger(__name__)


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

        with codecs.open(filePath, mode="r", encoding='shift_jis') as f:

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

    def _readFileHeader(self, data: dict):
        self.artist = data[b'ARTIST'] if b'ARTIST' in data.keys() else ""
        self.title = data[b'TITLE'] if b'TITLE' in data.keys() else ""
        self.version = data[b'PLAYLEVEL'] if b'PLAYLEVEL' in data.keys() else ""
        self.mode = data[b'PLAYER'] if b'PLAYER' in data.keys() else ""
        self.lnEndChannel = data[b'LNOBJ'] if b'LNOBJ' in data.keys() else b''

        # We do this to go in-line with the temporary measure property assigned in _readNotes.
        bpm = BMSBpm(0, bpm=int(data[b'BPM']))
        bpm.measure = 0

        log.debug(f"Added initial BPM {bpm.bpm}")
        self.bpms.append(bpm)

    @dataclass
    class _Hit:
        measure: float
        column: int

    @dataclass
    class _Hold:
        measure: float
        column: int
        tailMeasure: float

    @dataclass
    class _Bpm:
        measure: float
        bpm: int

    def _readNotes(self, data: List[dict], config: dict):

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
                            log.debug(f"Note at Col {configCase}, Measure {hitMeasure}")
                            hits.append(BMSMap._Hit(column=configCase, measure=hitMeasure))
                            hitMeasureHistory[configCase] = hitMeasure
                        else:  # This means we found an LN End, we have to look back to see which note is the head.
                            holdTMeasure = int(measureData['measure']) + i / length
                            log.debug(f"LN Tail at Col {configCase}, Measure {holdTMeasure}")
                            try:
                                holdHMeasure = hitMeasureHistory[configCase]
                                holds.append(BMSMap._Hold(column=configCase,
                                                          measure=holdHMeasure, tailMeasure=holdTMeasure))
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
        separately. So we get all possible unique measures, then map them to the measures.
        """

        # We will replace all item values as we loop through
        measures = dict(sorted({**{x.measure: 0 for x in hits},
                                **{x.measure: 0 for x in holds},
                                **{x.tailMeasure: 0 for x in holds}}.items()))

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
            self.notes.hits().append(BMSHit(offset=measures[hit.measure], column=hit.column))
        for hold in holds:
            self.notes.holds().append(BMSHold(offset=measures[hold.measure], column=hold.column,
                                              _length=measures[hold.tailMeasure] - measures[hold.measure]))

    def data(self) -> Dict[str, TimedList]:
        """ Gets the notes, bpms and svs as a dictionary """
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

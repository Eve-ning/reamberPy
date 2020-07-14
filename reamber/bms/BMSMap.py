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
from reamber.bms.BMSChannel import BMSChannel

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
    class _Note:
        measure: float
        column: int

    @dataclass
    class _Bpm:
        measure: float
        bpm: int

    def _readNotes(self, data: List[dict], config: dict):

        BEATS_PER_MEASURE = 4
        # The very first bpm is the one in the header, at 0th measure
        prevBpmMeasure = 0
        hits = []

        # Here we read all the notes, bpm changes as measures, we'll post process them later.
        for measureData in data:
            channel = measureData['channel']

            if channel in config.keys():
                slot = config[channel]

                # If it's an int, float, it's a note, else it'd be a str, which indicates BPM Change, Metronome change,
                # etc.
                if isinstance(slot, (float, int)):
                    seq = np.where([i != b'00' for i in measureData['sequence']])[0]
                    length = len(measureData['sequence'])
                    for i in seq:
                        log.debug(f"Note at Col {slot}, Measure {int(measureData['measure']) + i / length}")
                        hits.append(BMSMap._Note(column=slot, measure=int(measureData['measure']) + i / length))

                # This indicates the BPM Change
                elif slot == 'BPM_CHANGE':
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

        # Here we post-process the measures
        hits.sort(key=lambda x: x.measure)

        pass


    def data(self) -> Dict[str, TimedList]:
        """ Gets the notes, bpms and svs as a dictionary """
        return {'notes': self.notes,
                'bpms': self.bpms}

    def scrollSpeed(self, centerBpm: float = None) -> List[Dict[str, float]]:
        """ Evaluates the scroll speed based on mapType. Overrides the base to include SV
    
        e.g. if BPM == 200.0 and CenterBPM == 100.0, it'll return {'offset': X, 'speed': 2.0}

        :param centerBpm: The bpm to zero calculations on. If None, it'll just be the multiplication of bpm and sv.
        :return: Returns a list dict of keys offset and speed
        """
    
        # This automatically calculates the center BPM
        # Bpm Activity implicitly sorts
        if centerBpm is None: centerBpm = 1

        svPairs = [(offset, multiplier) for offset, multiplier in zip(self.svs.sorted().offsets(),
                                                                      self.svs.multipliers())]
        bpmPairs = [(offset, bpm) for offset, bpm in zip(self.bpms.offsets(), self.bpms.bpms())]
    
        currBpmIter = 0
        nextBpmOffset = None if len(bpmPairs) == 1 else bpmPairs[1][0]
        speedList = []
    
        for offset, sv in svPairs:
            while offset < bpmPairs[0][0]:  # Offset cannot be less than the first bpm
                continue
            # Guarantee that svOffset is after first bpm
            if nextBpmOffset and offset >= nextBpmOffset:
                currBpmIter += 1
                if currBpmIter != len(bpmPairs):
                    nextBpmOffset = bpmPairs[currBpmIter][0]
                else:
                    nextBpmOffset = None
            speedList.append(dict(offset=offset, speed=bpmPairs[currBpmIter][1] * sv / centerBpm))
    
        return speedList

    # noinspection PyMethodOverriding
    def metadata(self, unicode=True) -> str:
        """ Grabs the map metadata

        :param unicode: Whether to try to find the unicode or non-unicode. \
            This doesn't try to convert unicode to ascii, it just looks for if there's an available translation.
        :return:
        """

        def formatting(artist, title, difficulty, creator):
            return f"{artist} - {title}, {difficulty} ({creator})"

        return formatting(self.artist, self.title, self.version, self.creator)

    def rate(self, by: float, inplace:bool = False):
        """ Changes the rate of the map

        :param by: The value to rate it by. 1.1x speeds up the song by 10%. Hence 10/11 of the length.
        :param inplace: Whether to perform the operation in place. Returns a copy if False
        """
        this = self if inplace else self.deepcopy()
        super(BMSMap, this).rate(by=by, inplace=True)

        return None if inplace else this

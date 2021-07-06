from __future__ import annotations

from ctypes import Union
from dataclasses import dataclass, field
from typing import List

from reamber.base.MapSet import MapSet
from reamber.base.RAConst import RAConst
from reamber.sm.SMBpm import SMBpm
from reamber.sm.SMMap import SMMap
from reamber.sm.SMMapSetMeta import SMMapSetMeta
from reamber.sm.SMStop import SMStop
from reamber.sm.lists.SMBpmList import SMBpmList


@dataclass
class SMMapSet(SMMapSetMeta, MapSet):

    maps: List[SMMap] = field(default_factory=lambda: [])

    @staticmethod
    def read(lines: Union[str, List[str]]) -> SMMapSet:
        """ Reads a .sm file

        It reads all .sm as a mapset due to the nature of the file format.

        Note that it's best to just pass the .read as the argument.
        This uses a very specific splitting, not \\n.

        :param lines: The lines to the file.
        """
        self = SMMapSet()
        lines = "\n".join(lines) if isinstance(lines, list) else lines
        fileSpl = [i.strip() for i in lines.split(";")]
        metadata = []
        maps = []
        for token in fileSpl:
            if "#NOTES:" in token:
                maps.append(token)
            else:
                metadata.append(token)

        self._readMetadata(metadata)
        bpms = self._readBpms(offset=self.offset, lines=self._bpmsStr)
        self._readStops(lines=self._stopsStr, bpms=bpms)
        self._readMaps(maps=maps, bpms=bpms, stops=self.stops)

        for map in self.maps:
            map.bpms = bpms

        return self

    @staticmethod
    def readFile(filePath: str) -> SMMapSet:
        """ Reads a .sm file

        It reads all .sm as a mapset due to the nature of the file format.

        :param filePath: The path to the file
        """
        with open(filePath, "r", encoding="utf8") as f:
            file = f.read()

        # noinspection PyTypeChecker
        return SMMapSet.read(file)

    def writeFile(self, filePath: str,
                  alignBpms: bool = False,
                  BEAT_CORRECTION_FACTOR=5.0,
                  BEAT_ERROR_THRESHOLD=0.001):
        """ Writes the file to filePath specified

        :param BEAT_ERROR_THRESHOLD: See Bpm.py::alignBpms for details
        :param BEAT_CORRECTION_FACTOR: See Bpm.py::alignBpms for details
        :param filePath: File Path
        :param alignBpms: Aligns the BPM by mutating the current file. Details in Bpm.py
        """
        with open(filePath, "w+", encoding="utf8") as f:
            if alignBpms:
                for map in self.maps:
                    map.bpms = SMBpm.align_bpms(map.bpms,
                                                BEAT_CORRECTION_FACTOR=BEAT_CORRECTION_FACTOR,
                                                BEAT_ERROR_THRESHOLD=BEAT_ERROR_THRESHOLD)
            for s in self._writeMetadata(self.maps[0].bpms):
                f.write(s + "\n")

            for map in self.maps:
                assert isinstance(map, SMMap)
                for s in map.writeString():
                    f.write(s + "\n")

    @staticmethod
    def _readBpms(offset: float, lines: List[str]) -> SMBpmList:
        assert offset is not None, "Offset should be defined BEFORE Bpm"
        bpms = []
        beatPrev = 0.0
        bpmPrev = 1.0
        for line in lines:
            beatCurr, bpmCurr = [float(x.strip()) for x in line.split("=")]
            offset += (beatCurr - beatPrev) * RAConst.min_to_msec(1.0 / bpmPrev)
            bpms.append(SMBpm(offset=offset, bpm=bpmCurr))
            beatPrev = beatCurr
            bpmPrev = bpmCurr

        return SMBpmList(bpms)

    def _readStops(self, bpms: List[SMBpm], lines: List[str]):
        for line in lines:
            if len(line) == 0: return
            beatCurr, lengthCurr = [float(x.strip()) for x in line.split("=")]

            index = 0
            for index, bpm in enumerate(bpms):
                if bpm.beat(bpms) > beatCurr:
                    index -= 1
                    break

            offset = bpms[index].offset + (beatCurr - bpms[index].beat(bpms)) * bpms[index].beat_length()

            self.stops.append(SMStop(offset=offset, length=RAConst.sec_to_msec(lengthCurr)))

    def _readMaps(self, maps: List[str], bpms: List[SMBpm], stops: List[SMStop]):
        for map in maps:
            self.maps.append(SMMap.readString(noteStr=map, bpms=bpms, stops=stops))

    def rate(self, by: float, inplace:bool = False):
        """ Changes the rate of the map

        :param by: The value to rate it by. 1.1x speeds up the song by 10%. Hence 10/11 of the length.
        :param inplace: Whether to perform the operation in place. Returns a copy if False
        """
        this = self if inplace else self.deepcopy()
        super(SMMapSet, this).rate(by=by, inplace=True)

        # We invert it so it's easier to cast on Mult
        by = 1 / by
        this.sampleStart *= by
        this.sampleLength *= by

        return None if inplace else this

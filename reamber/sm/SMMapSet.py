from reamber.sm.SMMapSetMeta import SMMapSetMeta
from reamber.sm.lists.SMBpmList import SMBpmList
from reamber.sm.SMMap import SMMap
from reamber.sm.SMStop import SMStop
from dataclasses import dataclass, field
from reamber.sm.SMBpm import SMBpm

from reamber.base.RAConst import RAConst

from typing import List


@dataclass
class SMMapSet(SMMapSetMeta):

    maps: List[SMMap] = field(default_factory=lambda: [])

    def readFile(self, filePath: str):
        """ Reads a .sm file

        It reads all .sm as a mapset due to the nature of the file format.

        :param filePath: The path to the file
        """
        self.__init__()

        with open(filePath, "r", encoding="utf8") as f:
            file = f.read()
            fileSpl = file.split(";")
            metadata = []
            maps = []
            for index, line in enumerate(fileSpl):
                try:
                    line.index("#NOTES:")
                    maps.append(line)
                except ValueError:
                    metadata.append(line)

            self._readMetadata(metadata)
            bpms = self._readBpms(offset=self.offset, lines=self._bpmsStr)
            self._readStops(lines=self._stopsStr, bpms=bpms)
            self._readMaps(maps=maps, bpms=bpms, stops=self.stops)

            for map in self.maps:
                map.bpms = bpms
            return

    def writeFile(self, filePath: str,
                  alignBpms: bool = False,
                  BEAT_CORRECTION_FACTOR=5.0,
                  BEAT_ERROR_THRESHOLD=0.001):
        """
        Writes the file to filePath specified

        :param BEAT_ERROR_THRESHOLD: See Bpm.py::alignBpms for details
        :param BEAT_CORRECTION_FACTOR: See Bpm.py::alignBpms for details
        :param filePath: File Path
        :param alignBpms: Aligns the BPM by mutating the current file. Details in Bpm.py
        """
        with open(filePath, "w+", encoding="utf8") as f:
            if alignBpms:
                for map in self.maps:
                    map.bpms = SMBpm.alignBpms(map.bpms,
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
            offset += (beatCurr - beatPrev) * RAConst.minToMSec(1.0 / bpmPrev)
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

            offset = bpms[index].offset + (beatCurr - bpms[index].beat(bpms)) * bpms[index].beatLength()

            self.stops.append(SMStop(offset=offset, length=RAConst.secToMSec(lengthCurr)))

    def _readMaps(self, maps: List[str], bpms: List[SMBpm], stops: List[SMStop]):
        for map in maps:
            self.maps.append(SMMap.readString(noteStr=map, bpms=bpms, stops=stops))

    def describe(self, rounding: int = 2, unicode: bool = False) -> None:
        """ Describes the map's attributes as a short summary

        :param rounding: The decimal rounding
        :param unicode: Whether to attempt to get the non-unicode or unicode. \
            Doesn't attempt to translate.
        """

        for m in self.maps:
            m.describe(rounding=rounding, unicode=unicode, s=self)

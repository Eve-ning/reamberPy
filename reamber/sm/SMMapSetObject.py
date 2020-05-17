from reamber.base.MapSetObject import MapSetObject
from reamber.sm.SMMapSetObjectMeta import SMMapSetObjectMeta
from reamber.sm.SMMapObject import SMMapObject
from reamber.sm.SMStop import SMStop
from dataclasses import dataclass
from reamber.sm.SMBpmPoint import SMBpmPoint

from reamber.base.RAConst import RAConst

from typing import List


@dataclass
class SMMapSetObject(MapSetObject, SMMapSetObjectMeta):

    def readFile(self, filePath: str):
        with open(filePath, "r") as f:
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
                map.bpmPoints = bpms
            return

    def writeFile(self, filePath: str):
        with open(filePath, "w+") as f:
            for s in self._writeMetadata(self.maps[0].bpmPoints):
                f.write(s + "\n")

            for map in self.maps:
                assert isinstance(map, SMMapObject)
                for s in map.writeString(filePath=filePath):
                    f.write(s + "\n")

    @staticmethod
    def _readBpms(offset: float, lines: List[str]) -> List[SMBpmPoint]:
        assert offset is not None, "Offset should be defined BEFORE Bpm"
        bpms = []
        beatPrev = 0.0
        bpmPrev = 1.0
        for line in lines:
            beatCurr, bpmCurr = [float(x.strip()) for x in line.split("=")]
            offset += (beatCurr - beatPrev) * RAConst.minToMSec(1.0 / bpmPrev)
            bpms.append(SMBpmPoint(offset=offset, bpm=bpmCurr))
            beatPrev = beatCurr
            bpmPrev = bpmCurr

        return bpms

    def _readStops(self, bpms: List[SMBpmPoint], lines: List[str]):
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

    def _readMaps(self, maps: List[str], bpms: List[SMBpmPoint], stops: List[SMStop]):
        for map in maps:
            self.maps.append(SMMapObject.readString(map=map, bpms=bpms, stops=stops))

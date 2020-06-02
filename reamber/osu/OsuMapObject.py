from reamber.osu.OsuMapObjectMeta import OsuMapObjectMeta
from reamber.base.MapObject import MapObject

from reamber.osu.OsuTimingPointMeta import OsuTimingPointMeta
from reamber.osu.OsuBpmPoint import OsuBpmPoint
from reamber.osu.OsuSliderVelocity import OsuSliderVelocity

from reamber.osu.OsuHitObject import OsuHitObject
from reamber.osu.OsuHoldObject import OsuHoldObject
from reamber.osu.OsuNoteObjectMeta import OsuNoteObjectMeta

from typing import List
from dataclasses import dataclass
from dataclasses import field


@dataclass
class OsuMapObject(MapObject, OsuMapObjectMeta):

    svPoints: List[OsuSliderVelocity] = field(default_factory=lambda: [])

    def readFile(self, filePath=""):
        with open(filePath, "r", encoding="utf8") as f:
            file = f.read()
            file = file.replace("[TimingPoints]\n", "[HitObjects]\n")  # This is so as to split multiple delimiters
            fileSpl = file.split("[HitObjects]\n")
            if len(fileSpl) != 3:
                return

            self._readFileMetadata(fileSpl[0].split("\n"))

            for line in fileSpl[1].split("\n"):
                self._readFileTimingPoints(line)

            for line in fileSpl[2].split("\n"):
                self._readFileHitObjects(line)

    def writeFile(self, filePath=""):
        with open(filePath, "w+", encoding="utf8") as f:
            for s in self.writeStringList():
                f.write(s + "\n")

            f.write("\n[TimingPoints]\n")
            for tp in self.bpms:
                assert isinstance(tp, OsuBpmPoint)
                f.write(tp.writeString() + "\n")

            for tp in self.svPoints:
                assert isinstance(tp, OsuSliderVelocity)
                f.write(tp.writeString() + "\n")

            f.write("\n[HitObjects]\n")
            for ho in self.notes:
                assert isinstance(ho, (OsuHitObject, OsuHoldObject))
                f.write(ho.writeString(keys=int(self.circleSize)) + "\n")

    def _readFileMetadata(self, lines: List[str]):
        self.readStringList(lines)

    def _readFileTimingPoints(self, line: str):
        if OsuTimingPointMeta.isSliderVelocity(line):
            self.svPoints.append(OsuSliderVelocity.readString(line))
        elif OsuTimingPointMeta.isTimingPoint(line):
            self.bpms.append(OsuBpmPoint.readString(line))

    def _readFileHitObjects(self, line: str):
        if OsuNoteObjectMeta.isHitObject(line):
            self.notes.append(OsuHitObject.readString(line, int(self.circleSize)))
        elif OsuNoteObjectMeta.isHoldObject(line):
            self.notes.append(OsuHoldObject.readString(line, int(self.circleSize)))


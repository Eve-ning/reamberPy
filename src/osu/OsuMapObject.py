from src.osu.OsuMapObjectMeta import OsuMapObjectMeta
from src.osu.OsuSampleSet import OsuSampleSet
from src.base.MapObject import MapObject

from src.osu.OsuTimingPointMeta import OsuTimingPointMeta
from src.osu.OsuTimingPoint import OsuTimingPoint
from src.osu.OsuSliderVelocity import OsuSliderVelocity

from src.osu.OsuHitObject import OsuHitObject
from src.osu.OsuHoldObject import OsuHoldObject
from src.osu.OsuHitObjectMeta import OsuHitObjectMeta

from typing import List
from dataclasses import dataclass


@dataclass
class OsuMapObject(MapObject, OsuMapObjectMeta):

    def readFile(self, filePath=""):
        with open(filePath, "r") as f:
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
        with open(filePath, "w+") as f:
            for s in self.writeStringList():
                f.write(s + "\n")

            f.write("\n[TimingPoints]\n")
            for tp in self.timingPoints:
                f.write(tp.writeString() + "\n")

            f.write("\n[HitObjects]\n")
            for ho in self.hitObjects:
                f.write(ho.writeString(keys=self.circleSize) + "\n")

    def _readFileMetadata(self, lines: List[str]):
        self.readStringList(lines)

    def _readFileTimingPoints(self, line: str):
        if OsuTimingPointMeta.isSliderVelocity(line):
            self.timingPoints.append((OsuSliderVelocity.readString(line)))
        elif OsuTimingPointMeta.isTimingPoint(line):
            self.timingPoints.append((OsuTimingPoint.readString(line)))

    def _readFileHitObjects(self, line: str):
        if OsuHitObjectMeta.isHitObject(line):
            self.hitObjects.append((OsuHitObject.readString(line, int(self.circleSize))))
        elif OsuHitObjectMeta.isHoldObject(line):
            self.hitObjects.append((OsuHoldObject.readString(line, int(self.circleSize))))






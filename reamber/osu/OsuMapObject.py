from reamber.osu.OsuMapObjectMeta import OsuMapObjectMeta
from reamber.base.MapObject import MapObject
from reamber.osu.lists.OsuSvList import OsuSvList

from reamber.osu.OsuTimingPointMeta import OsuTimingPointMeta
from reamber.osu.OsuBpmObject import OsuBpmObject
from reamber.osu.OsuSvObject import OsuSvObject
from reamber.osu.OsuHitObject import OsuHitObject
from reamber.osu.OsuHoldObject import OsuHoldObject
from reamber.osu.OsuNoteObjectMeta import OsuNoteObjectMeta

from typing import List
from dataclasses import dataclass, field

from reamber.osu.lists.OsuNotePkg import OsuNotePkg
from reamber.osu.lists.OsuBpmList import OsuBpmList


@dataclass
class OsuMapObject(MapObject, OsuMapObjectMeta):

    notes: OsuNotePkg = field(default_factory=lambda: OsuNotePkg())
    bpms:  OsuBpmList  = field(default_factory=lambda: OsuBpmList())
    svs:   OsuSvList   = field(default_factory=lambda: OsuSvList())

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
                assert isinstance(tp, OsuBpmObject)
                f.write(tp.writeString() + "\n")

            for tp in self.svs:
                assert isinstance(tp, OsuSvObject)
                f.write(tp.writeString() + "\n")

            f.write("\n[HitObjects]\n")
            for ho in self.notes.hits:
                f.write(ho.writeString(keys=int(self.circleSize)) + "\n")

            for ho in self.notes.holds:
                f.write(ho.writeString(keys=int(self.circleSize)) + "\n")

    def _readFileMetadata(self, lines: List[str]):
        self.readStringList(lines)

    def _readFileTimingPoints(self, line: str):
        if OsuTimingPointMeta.isSliderVelocity(line):
            self.svs.append(OsuSvObject.readString(line))
        elif OsuTimingPointMeta.isTimingPoint(line):
            self.bpms.append(OsuBpmObject.readString(line))

    def _readFileHitObjects(self, line: str):
        if OsuNoteObjectMeta.isHitObject(line):
            self.notes.hits.append(OsuHitObject.readString(line, int(self.circleSize)))
        elif OsuNoteObjectMeta.isHoldObject(line):
            self.notes.holds.append(OsuHoldObject.readString(line, int(self.circleSize)))

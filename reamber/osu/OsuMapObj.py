from reamber.osu.OsuMapObjMeta import OsuMapObjMeta
from reamber.base.MapObj import MapObj
from reamber.osu.lists.OsuSvList import OsuSvList

from reamber.osu.OsuTimingPointMeta import OsuTimingPointMeta
from reamber.osu.OsuBpmObj import OsuBpmObj
from reamber.osu.OsuSvObj import OsuSvObj
from reamber.osu.OsuHitObj import OsuHitObj
from reamber.osu.OsuHoldObj import OsuHoldObj
from reamber.osu.OsuNoteObjMeta import OsuNoteObjMeta

from typing import List
from dataclasses import dataclass, field

from reamber.osu.lists.OsuNotePkg import OsuNotePkg
from reamber.osu.lists.OsuBpmList import OsuBpmList


@dataclass
class OsuMapObj(MapObj, OsuMapObjMeta):

    notes: OsuNotePkg = field(default_factory=lambda: OsuNotePkg())
    bpms:  OsuBpmList  = field(default_factory=lambda: OsuBpmList())
    svs:   OsuSvList   = field(default_factory=lambda: OsuSvList())

    def readFile(self, filePath=""):
        with open(filePath, "r", encoding="utf8") as f:
            file = f.read()
            file = file.replace("[TimingPoints]\n", "[HitObjs]\n")  # This is so as to split multiple delimiters
            fileSpl = file.split("[HitObjs]\n")
            if len(fileSpl) != 3:
                return

            self._readFileMetadata(fileSpl[0].split("\n"))

            for line in fileSpl[1].split("\n"):
                self._readFileTimingPoints(line)

            for line in fileSpl[2].split("\n"):
                self._readFileHitObjs(line)

    def writeFile(self, filePath=""):
        with open(filePath, "w+", encoding="utf8") as f:
            for s in self.writeStringList():
                f.write(s + "\n")

            f.write("\n[TimingPoints]\n")
            for tp in self.bpms:
                assert isinstance(tp, OsuBpmObj)
                f.write(tp.writeString() + "\n")

            for tp in self.svs:
                assert isinstance(tp, OsuSvObj)
                f.write(tp.writeString() + "\n")

            f.write("\n[HitObjs]\n")
            for ho in self.notes.hits:
                f.write(ho.writeString(keys=int(self.circleSize)) + "\n")

            for ho in self.notes.holds:
                f.write(ho.writeString(keys=int(self.circleSize)) + "\n")

    def _readFileMetadata(self, lines: List[str]):
        self.readStringList(lines)

    def _readFileTimingPoints(self, line: str):
        if OsuTimingPointMeta.isSliderVelocity(line):
            self.svs.append(OsuSvObj.readString(line))
        elif OsuTimingPointMeta.isTimingPoint(line):
            self.bpms.append(OsuBpmObj.readString(line))

    def _readFileHitObjs(self, line: str):
        if OsuNoteObjMeta.isHitObj(line):
            self.notes.hits.append(OsuHitObj.readString(line, int(self.circleSize)))
        elif OsuNoteObjMeta.isHoldObj(line):
            self.notes.holds.append(OsuHoldObj.readString(line, int(self.circleSize)))

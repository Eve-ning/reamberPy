from reamber.osu.OsuMapMeta import OsuMapMeta
from reamber.base.Map import Map
from reamber.osu.lists.OsuSvList import OsuSvList

from reamber.osu.OsuTimingPointMeta import OsuTimingPointMeta
from reamber.osu.OsuBpm import OsuBpm
from reamber.osu.OsuSv import OsuSv
from reamber.osu.OsuHit import OsuHit
from reamber.osu.OsuHold import OsuHold
from reamber.osu.OsuNoteMeta import OsuNoteMeta

from typing import List, Dict
from dataclasses import dataclass, field

from reamber.osu.lists.OsuNotePkg import OsuNotePkg
from reamber.osu.lists.OsuBpmList import OsuBpmList
from reamber.osu.OsuSampleSet import OsuSampleSet
from reamber.base.lists.TimedList import TimedList

@dataclass
class OsuMap(Map, OsuMapMeta):

    notes: OsuNotePkg = field(default_factory=lambda: OsuNotePkg())
    bpms:  OsuBpmList = field(default_factory=lambda: OsuBpmList())
    svs:   OsuSvList  = field(default_factory=lambda: OsuSvList())

    def data(self) -> Dict[str, TimedList]:
        """ Gets the notes, bpms and svs as a dictionary """
        return {'notes': self.notes,
                'bpms': self.bpms,
                'svs': self.svs}

    def resetAllSamples(self, notes=True, samples=True) -> None:
        """ Resets all hitsounds and samples

        :param notes: Whether to reset hitsounds on notes
        :param samples: Whether to reset samples
        """
        if notes:
            for n in self.notes.hits():
                n.hitsoundFile = ""
                n.sampleSet = OsuSampleSet.AUTO
                n.hitsoundSet = OsuSampleSet.AUTO
                n.customSet = OsuSampleSet.AUTO
                n.additionSet = OsuSampleSet.AUTO

            for n in self.notes.holds():
                n.hitsoundFile = ""
                n.sampleSet = OsuSampleSet.AUTO
                n.hitsoundSet = OsuSampleSet.AUTO
                n.customSet = OsuSampleSet.AUTO
                n.additionSet = OsuSampleSet.AUTO

        if samples: self.samples.clear()

    def readFile(self, filePath=""):
        """ Reads a .osu, loads inplace, hence it doesn't return anything

        :param filePath: The path to the .osu file."""

        self.__init__()

        with open(filePath, "r", encoding="utf8") as f:
            file = f.read()
            file = file.replace("[TimingPoints]\n", "[HitObjects]\n")  # This is so as to split multiple delimiters
            fileSpl = file.split("[HitObjects]\n")
            if len(fileSpl) != 3:
                raise Exception("Incorrect File Format")

            self._readFileMetadata(fileSpl[0].split("\n"))

            for line in fileSpl[1].split("\n"):
                self._readFileTimingPoints(line)

            for line in fileSpl[2].split("\n"):
                self._readFileHitObjects(line)

    def writeFile(self, filePath=""):
        """ Writes a .osu, doesn't return anything.

        :param filePath: The path to a new .osu file."""

        with open(filePath, "w+", encoding="utf8") as f:
            for s in self.writeStringList():
                f.write(s + "\n")

            f.write("\n[TimingPoints]\n")
            for tp in self.bpms:
                assert isinstance(tp, OsuBpm)
                f.write(tp.writeString() + "\n")

            for tp in self.svs:
                assert isinstance(tp, OsuSv)
                f.write(tp.writeString() + "\n")

            f.write("\n[HitObjects]\n")
            for ho in self.notes.hits():
                f.write(ho.writeString(keys=int(self.circleSize)) + "\n")

            for ho in self.notes.holds():
                f.write(ho.writeString(keys=int(self.circleSize)) + "\n")

    def _readFileMetadata(self, lines: List[str]):
        """ Reads the metadata only, inclusive of Events """
        self.readStringList(lines)

    def _readFileTimingPoints(self, line: str):
        """ Reads all TimingPoints """
        if OsuTimingPointMeta.isSliderVelocity(line):
            self.svs.append(OsuSv.readString(line))
        elif OsuTimingPointMeta.isTimingPoint(line):
            self.bpms.append(OsuBpm.readString(line))

    def _readFileHitObjects(self, line: str):
        """ Reads all HitObjects """
        if OsuNoteMeta.isHit(line):
            self.notes.hits().append(OsuHit.readString(line, int(self.circleSize)))
        elif OsuNoteMeta.isHold(line):
            self.notes.holds().append(OsuHold.readString(line, int(self.circleSize)))

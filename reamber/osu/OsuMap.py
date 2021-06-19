from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Union

from reamber.base.Map import Map
from reamber.base.lists.TimedList import TimedList
from reamber.osu.OsuBpm import OsuBpm
from reamber.osu.OsuHit import OsuHit
from reamber.osu.OsuHold import OsuHold
from reamber.osu.OsuMapMeta import OsuMapMeta
from reamber.osu.OsuNoteMeta import OsuNoteMeta
from reamber.osu.OsuSampleSet import OsuSampleSet
from reamber.osu.OsuSv import OsuSv
from reamber.osu.OsuTimingPointMeta import OsuTimingPointMeta
from reamber.osu.lists.OsuBpmList import OsuBpmList
from reamber.osu.lists.OsuNotePkg import OsuNotePkg
from reamber.osu.lists.OsuSvList import OsuSvList


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

    @staticmethod
    def read(lines: List[str]) -> OsuMap:
        """ Reads a .osu, loads inplace, hence it doesn't return anything

        :param lines: The lines to the .osu file."""

        self = OsuMap()
        lines = [line.strip() for line in lines]  # Redundancy for safety

        try:
            ix_tp = lines.index("[TimingPoints]")
            ix_ho = lines.index("[HitObjects]")
        except ValueError:
            raise Exception("Incorrect File Format. Cannot find [TimingPoints] or [HitObjects].")

        self._readFileMetadata(lines[:ix_tp])
        self._readFileTimingPoints(lines[ix_tp+1:ix_ho])
        self._readFileHitObjects(lines[ix_ho+1:])

        return self



    @staticmethod
    def readFile(filePath: str) -> OsuMap:
        """ Reads a .osu, loads inplace, hence it doesn't return anything

        :param filePath: The path to the .osu file."""

        with open(filePath, "r", encoding="utf8") as f:
            # We read the file and firstly find the distinct sections
            # 1) Meta 2) Timing Points 3) Hit Objects

            file = [i.strip() for i in f.read().split("\n")]

        return OsuMap.read(lines=file)

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

    def _readFileTimingPoints(self, lines: Union[List[str], str]):
        """ Reads all TimingPoints """
        lines = lines if isinstance(lines, list) else [lines]
        for line in lines:
            if OsuTimingPointMeta.isSliderVelocity(line):
                self.svs.append(OsuSv.readString(line))
            elif OsuTimingPointMeta.isTimingPoint(line):
                self.bpms.append(OsuBpm.readString(line))

    def _readFileHitObjects(self, lines: Union[List[str], str]):
        """ Reads all HitObjects """
        lines = lines if isinstance(lines, list) else [lines]
        for line in lines:
            if OsuNoteMeta.isHit(line):
                self.notes.hits().append(OsuHit.readString(line, int(self.circleSize)))
            elif OsuNoteMeta.isHold(line):
                self.notes.holds().append(OsuHold.readString(line, int(self.circleSize)))

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

        if unicode: return formatting(self.artistUnicode, self.titleUnicode, self.version, self.creator)
        else: return formatting(self.artist, self.title, self.version, self.creator)

    def rate(self, by: float, inplace:bool = False):
        """ Changes the rate of the map

        :param by: The value to rate it by. 1.1x speeds up the song by 10%. Hence 10/11 of the length.
        :param inplace: Whether to perform the operation in place. Returns a copy if False
        """
        this = self if inplace else self.deepcopy()
        super(OsuMap, this).rate(by=by, inplace=True)

        # We invert it so it's easier to cast on Mult
        by = 1 / by
        this.samples.multOffset(by=by, inplace=True)
        this.previewTime *= by

        return None if inplace else this

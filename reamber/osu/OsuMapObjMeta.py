from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
from reamber.osu.OsuSampleSet import OsuSampleSet
from reamber.osu.OsuSampleObj import OsuSampleObj
from reamber.osu.lists.OsuSampleList import OsuSampleList


class OsuMapObjMode:
    STANDARD: int = 0
    TAIKO: int = 1
    CATCH: int = 2
    MANIA: int = 3


@dataclass
class OsuMapObjMetaGeneral:
    audioFileName: str = ""
    audioLeadIn: int = 0
    previewTime: int = -1
    countdown: bool = False
    sampleSet: int = OsuSampleSet.AUTO
    stackLeniency: float = 0.7
    mode: int = OsuMapObjMode.MANIA
    letterboxInBreaks: bool = False
    specialStyle: bool = False
    widescreenStoryboard: bool = True


@dataclass
class OsuMapObjMetaEditor:
    distanceSpacing: float = 4
    beatDivisor: int = 4
    gridSize: int = 8
    timelineZoom: float = 0.3


@dataclass
class OsuMapObjMetaMetadata:
    title: str = ""
    titleUnicode: str = ""
    artist: str = ""
    artistUnicode: str = ""
    creator: str = ""
    version: str = ""
    source: str = ""
    tags: List[str] = ""
    beatmapID: int = 0
    beatmapSetID: int = -1


@dataclass
class OsuMapObjMetaDifficulty:
    hpDrainRate: float = 5.0
    circleSize: float = 4.0
    overallDifficulty: float = 5.0
    approachRate: float = 5.0
    sliderMultiplier: float = 1.4
    sliderTickRate: int = 1


@dataclass
class OsuMapObjMetaEvents:
    backgroundFileName: str = ""
    samples: OsuSampleList = field(default_factory=lambda: OsuSampleList())


@dataclass
class OsuMapObjMeta(OsuMapObjMetaGeneral,
                       OsuMapObjMetaEditor,
                       OsuMapObjMetaMetadata,
                       OsuMapObjMetaDifficulty,
                       OsuMapObjMetaEvents):

    def readStringList(self, lines: List[str]):
        for index, line in enumerate(lines):
            if line == "":
                continue

            s = line.split(":")
            if s[0] == "AudioFilename":             self.audioFileName = s[1].strip()
            elif s[0] == "AudioLeadIn":             self.audioLeadIn = int(s[1])
            elif s[0] == "PreviewTime":             self.previewTime = int(s[1])
            elif s[0] == "Countdown":               self.countdown = bool(s[1])
            elif s[0] == "SampleSet":               self.sampleSet = OsuSampleSet.fromString(s[1].strip())
            elif s[0] == "StackLeniency":           self.stackLeniency = float(s[1])
            elif s[0] == "Mode":                    self.mode = int(s[1])
            elif s[0] == "LetterboxInBreaks":       self.letterboxInBreaks = bool(s[1])
            elif s[0] == "SpecialStyle":            self.specialStyle = bool(s[1])
            elif s[0] == "WidescreenStoryboard":    self.widescreenStoryboard = bool(s[1])
            elif s[0] == "DistanceSpacing":         self.distanceSpacing = float(s[1])
            elif s[0] == "BeatDivisor":             self.beatDivisor = int(s[1])
            elif s[0] == "GridSize":                self.gridSize = int(s[1])
            elif s[0] == "TimelineZoom":            self.timelineZoom = float(s[1])
            elif s[0] == "Title":                   self.title = s[1].strip()
            elif s[0] == "TitleUnicode":            self.titleUnicode = s[1].strip()
            elif s[0] == "Artist":                  self.artist = s[1].strip()
            elif s[0] == "ArtistUnicode":           self.artistUnicode = s[1].strip()
            elif s[0] == "Creator":                 self.creator = s[1].strip()
            elif s[0] == "Version":                 self.version = s[1].strip()
            elif s[0] == "Source":                  self.source = s[1].strip()
            elif s[0] == "Tags":                    self.tags = [i.strip() for i in s[1].split(",")]
            elif s[0] == "BeatmapID":               self.beatmapID = int(s[1])
            elif s[0] == "BeatmapSetID":            self.beatmapSetID = int(s[1])
            elif s[0] == "HPDrainRate":             self.hpDrainRate = float(s[1])
            elif s[0] == "CircleSize":              self.circleSize = float(s[1])
            elif s[0] == "OverallDifficulty":       self.overallDifficulty = float(s[1])
            elif s[0] == "ApproachRate":            self.approachRate = float(s[1])
            elif s[0] == "SliderMultiplier":        self.sliderMultiplier = float(s[1])
            elif s[0] == "SliderTickRate":          self.sliderTickRate = int(s[1])

            if s[0] == "//Background and Video events":
                line = lines[index + 1]
                self.backgroundFileName = line[line.find('"')+1:line.rfind('"')]

            if s[0] == "//Storyboard Sound Samples":
                for sampLine in lines[index + 1:]:
                    if not sampLine.startswith('Sample'): break
                    self.samples.append(OsuSampleObj.readString(sampLine))
                break

    def writeStringList(self) -> List[str]:
        return [
            "osu file format v14",
            "",
            "[General]",
            f"AudioFilename: {self.audioFileName}",
            f"AudioLeadIn: {self.audioLeadIn}",
            f"PreviewTime: {self.previewTime}",
            f"Countdown: {int(self.countdown)}",
            f"SampleSet: {self.sampleSet}",
            f"StackLeniency: {self.stackLeniency}",
            f"Mode: {self.mode}",
            f"LetterboxInBreaks: {int(self.letterboxInBreaks)}",
            f"SpecialStyle: {int(self.specialStyle)}",
            f"WidescreenStoryboard: {int(self.widescreenStoryboard)}",
            "",
            "[Editor]",
            f"DistanceSpacing: {self.distanceSpacing}",
            f"BeatDivisor: {self.beatDivisor}",
            f"GridSize: {self.gridSize}",
            f"TimelineZoom: {self.timelineZoom}",
            "",
            "[Metadata]",
            f"Title:{self.title}",
            f"TitleUnicode:{self.titleUnicode}",
            f"Artist:{self.artist}",
            f"ArtistUnicode:{self.artistUnicode}",
            f"Creator:{self.creator}",
            f"Version:{self.version}",
            f"Source:{self.source}",
            f"Tags:{', '.join(self.tags)}",
            f"BeatmapID:{self.beatmapID}",
            f"BeatmapSetID:{self.beatmapSetID}",
            "",
            "[Difficulty]",
            f"HPDrainRate:{self.hpDrainRate}",
            f"CircleSize:{self.circleSize}",
            f"OverallDifficulty:{self.overallDifficulty}",
            f"ApproachRate:{self.approachRate}",
            f"SliderMultiplier:{self.sliderMultiplier}",
            f"SliderTickRate:{self.sliderTickRate}",
            "",
            "[Events]",
            "//Background and Video events",
            f"0,0,\"{self.backgroundFileName}\",0,0",
            "//Break Periods",
            "//Storyboard Layer 0 (Background)",
            "//Storyboard Layer 1 (Fail)",
            "//Storyboard Layer 2 (Pass)",
            "//Storyboard Layer 3 (Foreground)",
            "//Storyboard Layer 4 (Overlay)",
            "//Storyboard Sound Samples",
            *[sample.writeString() for sample in self.samples]
        ]

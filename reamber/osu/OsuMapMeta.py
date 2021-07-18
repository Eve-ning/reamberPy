from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from unidecode import unidecode

from reamber.osu.OsuSample import OsuSample
from reamber.osu.OsuSampleSet import OsuSampleSet
from reamber.osu.lists.OsuSampleList import OsuSampleList


class OsuMapMode:
    """ This determines the mode of the map.

    Note that only MANIA is supported for now.
    """
    STANDARD: int = 0
    TAIKO: int = 1
    CATCH: int = 2
    MANIA: int = 3


@dataclass
class OsuMapMetaGeneral:
    """ All meta under [General] """

    audio_file_name: str = ""
    audio_lead_in: int = 0
    preview_time: int = -1
    countdown: bool = False
    sample_set: int = OsuSampleSet.AUTO
    stack_leniency: float = 0.7
    mode: int = OsuMapMode.MANIA
    letterbox_in_breaks: bool = False
    special_style: bool = False
    widescreen_storyboard: bool = True


@dataclass
class OsuMapMetaEditor:
    """ All meta under [Editor] """

    distance_spacing: float = 4
    beat_divisor: int = 4
    grid_size: int = 8
    timeline_zoom: float = 0.3


@dataclass
class OsuMapMetaMetadata:
    """ All meta under [Metadata] """

    title: str = ""
    title_unicode: str = ""
    artist: str = ""
    artist_unicode: str = ""
    creator: str = ""
    version: str = ""
    source: str = ""
    tags: List[str] = ""
    beatmap_id: int = 0
    beatmap_set_id: int = -1


@dataclass
class OsuMapMetaDifficulty:
    """ All meta under [Difficulty] """

    hp_drain_rate: float = 5.0
    circle_size: float = 4.0
    overall_difficulty: float = 5.0
    approach_rate: float = 5.0
    slider_multiplier: float = 1.4
    slider_tick_rate: int = 1


@dataclass
class OsuMapMetaEvents:
    """ All meta under [Events], Excludes Storyboard. """

    background_file_name: str = ""
    samples: OsuSampleList = field(default_factory=lambda: OsuSampleList([]))


@dataclass
class OsuMapMeta(OsuMapMetaGeneral,
                 OsuMapMetaEditor,
                 OsuMapMetaMetadata,
                 OsuMapMetaDifficulty,
                 OsuMapMetaEvents):
    """ The umbrella class that holds everything not included in HitObjects and TimingPoints """

    def _read_meta_string_list(self, lines: List[str]):
        """ Reads everything Meta """
        for index, line in enumerate(lines):
            if line == "":
                continue

            s = line.split(":")
            if s[0] == "AudioFilename":          self.audio_file_name       = s[1].strip()
            elif s[0] == "AudioLeadIn":          self.audio_lead_in         = int(s[1])
            elif s[0] == "PreviewTime":          self.preview_time          = int(s[1])
            elif s[0] == "Countdown":            self.countdown             = bool(int(s[1]))
            elif s[0] == "SampleSet":            self.sample_set            = OsuSampleSet.from_string(s[1].strip())
            elif s[0] == "StackLeniency":        self.stack_leniency        = float(s[1])
            elif s[0] == "Mode":                 self.mode                  = int(s[1])
            elif s[0] == "LetterboxInBreaks":    self.letterbox_in_breaks   = bool(int(s[1]))
            elif s[0] == "SpecialStyle":         self.special_style         = bool(int(s[1]))
            elif s[0] == "WidescreenStoryboard": self.widescreen_storyboard = bool(int(s[1]))
            elif s[0] == "DistanceSpacing":      self.distance_spacing      = float(s[1])
            elif s[0] == "BeatDivisor":          self.beat_divisor          = int(s[1])
            elif s[0] == "GridSize":             self.grid_size             = int(s[1])
            elif s[0] == "TimelineZoom":         self.timeline_zoom         = float(s[1])
            elif s[0] == "Title":                self.title                 = s[1].strip()
            elif s[0] == "TitleUnicode":         self.title_unicode         = s[1].strip()
            elif s[0] == "Artist":               self.artist                = s[1].strip()
            elif s[0] == "ArtistUnicode":        self.artist_unicode        = s[1].strip()
            elif s[0] == "Creator":              self.creator               = s[1].strip()
            elif s[0] == "Version":              self.version               = s[1].strip()
            elif s[0] == "Source":               self.source                = s[1].strip()
            elif s[0] == "Tags":                 self.tags                  = [i.strip() for i in s[1].split(" ") if i]
            elif s[0] == "BeatmapID":            self.beatmap_id            = int(s[1])
            elif s[0] == "BeatmapSetID":         self.beatmap_set_id        = int(s[1])
            elif s[0] == "HPDrainRate":          self.hp_drain_rate         = float(s[1])
            elif s[0] == "CircleSize":           self.circle_size           = float(s[1])
            elif s[0] == "OverallDifficulty":    self.overall_difficulty    = float(s[1])
            elif s[0] == "ApproachRate":         self.approach_rate         = float(s[1])
            elif s[0] == "SliderMultiplier":     self.slider_multiplier     = float(s[1])
            elif s[0] == "SliderTickRate":       self.slider_tick_rate      = int(s[1])

            if s[0] == "//Background and Video events":
                line = lines[index + 1]
                self.background_file_name = line[line.find('"') + 1:line.rfind('"')]

            if s[0] == "//Storyboard Sound Samples":
                self.samples = OsuSampleList.read(
                    [line for line in lines[index+1:] if line.startswith('Sample')]
                )

    def write_meta_string_list(self) -> List[str]:
        """ Writes everything Meta """
        return [
            "osu file format v14",
            "",
            "[General]",
            f"AudioFilename: {self.audio_file_name}",
            f"AudioLeadIn: {self.audio_lead_in:g}",
            f"PreviewTime: {int(self.preview_time)}",
            f"Countdown: {int(self.countdown)}",
            f"SampleSet: {self.sample_set}",
            f"StackLeniency: {self.stack_leniency}",
            f"Mode: {self.mode}",
            f"LetterboxInBreaks: {int(self.letterbox_in_breaks)}",
            f"SpecialStyle: {int(self.special_style)}",
            f"WidescreenStoryboard: {int(self.widescreen_storyboard)}",
            "",
            "[Editor]",
            f"DistanceSpacing: {self.distance_spacing:g}",
            f"BeatDivisor: {self.beat_divisor:g}",
            f"GridSize: {self.grid_size:g}",
            f"TimelineZoom: {self.timeline_zoom:g}",
            "",
            "[Metadata]",
            f"Title:{unidecode(self.title)}",
            f"TitleUnicode:{self.title_unicode}",
            f"Artist:{unidecode(self.artist)}",
            f"ArtistUnicode:{self.artist_unicode}",
            f"Creator:{self.creator}",
            f"Version:{self.version}",
            f"Source:{self.source}",
            f"Tags:{' '.join(self.tags)}",
            f"BeatmapID:{self.beatmap_id}",
            f"BeatmapSetID:{self.beatmap_set_id}",
            "",
            "[Difficulty]",
            f"HPDrainRate:{self.hp_drain_rate:g}",
            f"CircleSize:{self.circle_size:g}",
            f"OverallDifficulty:{self.overall_difficulty:g}",
            f"ApproachRate:{self.approach_rate:g}",
            f"SliderMultiplier:{self.slider_multiplier:g}",
            f"SliderTickRate:{self.slider_tick_rate:g}",
            "",
            "[Events]",
            "//Background and Video events",
            f"0,0,\"{self.background_file_name}\",0,0",
            "//Break Periods",
            "//Storyboard Layer 0 (Background)",
            "//Storyboard Layer 1 (Fail)",
            "//Storyboard Layer 2 (Pass)",
            "//Storyboard Layer 3 (Foreground)",
            "//Storyboard Layer 4 (Overlay)",
            "//Storyboard Sound Samples",
            *[sample.write_string() for sample in self.samples]  # Unpacks all samples
        ]

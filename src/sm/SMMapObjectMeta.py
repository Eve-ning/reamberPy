from dataclasses import dataclass
from dataclasses import field
from typing import List


class SMMapObjectDifficulty:
    BEGINNER: str = "Beginner"
    EASY: str = "Easy"
    MEDIUM: str = "Medium"
    HARD: str = "Hard"
    CHALLENGE: str = "Challenge"
    EDIT: str = "Edit"


class SMMapObjectChartTypes:
    # Full Description in CHART_TYPES
    DANCE_SINGLE: str = "dance-single"          # Your normal 4 panel dance mode.
    DANCE_DOUBLE: str = "dance-double"          # Both P1 & P2 pads are used for one player.
    DANCE_SOLO: str = "dance-solo"              # 4-panel, except with additional top-left and top-right columns.
    DANCE_COUPLE: str = "dance-couple"          # One chart, but P1 & P2 have different steps.
    DANCE_THREEPANEL: str = "dance-threepanel"  # Like Single, but the down arrow isn't used.
    DANCE_ROUTINE: str = "dance-routine"        # It's like Couple in that it's for two players
    PUMP_SINGLE: str = "pump-single"            # Single, 5-panel pad.
    PUMP_HALFDOUBLE: str = "pump-halfdouble"    # Uses only six panels in the middle of the pad
    PUMP_DOUBLE: str = "pump-double"            # Same as Dance.
    PUMP_COUPLE: str = "pump-couple"            # Same as Dance.
    PUMP_ROUTINE: str = "pump-routine"          # Same as Dance.
    KB7_SINGLE: str = "kb7-single"              # Standard kb7 layout
    KICKBOX_HUMAN: str = "kickbox-human"        # 4key
    KICKBOX_QUADARM: str = "kickbox-quadarm"    # 4key
    KICKBOX_INSECT: str = "kickbox-insect"      # 6key
    KICKBOX_ARACHNID: str = "kickbox-arachnid"  # 8key
    PARA_SINGLE: str = "para-single"            # 5key.
    BM_SINGLE5: str = "bm-single5"              # 5+1key game mode
    BM_VERSUS5: str = "bm-versus5"              # Unknown, might be the beat equivalent to Couple?
    BM_DOUBLE5: str = "bm-double5"              # Both sides are used.
    BM_SINGLE7: str = "bm-single7"              # 7+1key game mode
    BM_DOUBLE7: str = "bm-double7"              # Both sides are used.
    BM_VERSUS7: str = "bm-versus7"              # Unknown (see versus5)
    EZ2_SINGLE: str = "ez2-single"              # 1 pad
    EZ2_DOUBLE: str = "ez2-double"              # 2 pad
    EZ2_REAL: str = "ez2-real"                  # Divides the hand sensors into upper and lower halves.
    PNM_FIVE: str = "pnm-five"                  # 5key game mode.
    PNM_NINE: str = "pnm-nine"                  # 9key game mode.
    TECHNO_SINGLE4: str = "techno-single4"      # Identical to dance_single
    TECHNO_SINGLE5: str = "techno-single5"      # Identical to pump_single
    TECHNO_SINGLE8: str = "techno-single8"      # eight panels are used: ⬅⬇⬆➡↙↘↗↖
    TECHNO_DOUBLE4: str = "techno-double4"      # Identical to dance_double
    TECHNO_DOUBLE5: str = "techno-double5"      # Identical to pump_double
    TECHNO_DOUBLE8: str = "techno-double8"      # 16 panels (doubles)
    DS3DDX_SINGLE: str = "ds3ddx-single"        # 4key + 4hand...
    MANIAX_SINGLE: str = "maniax-single"        # 4key
    MANIAX_DOUBLE: str = "maniax-double"        # 8key


@dataclass
class SMMapObjectMeta:
    title: str = ""
    subtitle: str = ""
    artist: str = ""
    titleTranslit: str = ""
    subtitleTranslit: str = ""
    artistTranslit: str = ""
    genre: str = ""
    credit: str = ""
    banner: str = ""
    background: str = ""
    lyricsPath: str = ""
    cdTitle: str = ""
    music: str = ""
    offset: float = 0.0
    # BPMS
    # STOPS
    sampleStart: float = 0.0
    sampleLength: float = 0.0
    displayBpm: str = ""
    selectable: bool = True
    bgChanges: str = ""  # Idk what this does
    fgChanges: str = ""  # Idk what this does

    chartType: str = SMMapObjectChartTypes.DANCE_SINGLE
    description: str = ""
    difficulty: str = SMMapObjectDifficulty.EASY
    difficultyVal: int = 1
    grooveRadar: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0, 0.0, 0.0])

    def _readMetadata(self, lines: List[str]):
        for line in lines:
            if line == "":
                continue

            s = line.split(":")

            if   s[0] == "#TITLE":              self.title = s[1].strip()[:-1]
            elif s[0] == "#SUBTITLE":           self.subtitle = s[1].strip()[:-1]
            elif s[0] == "#ARTIST":             self.artist = s[1].strip()[:-1]
            elif s[0] == "#TITLETRANSLIT":      self.titleTranslit = s[1].strip()[:-1]
            elif s[0] == "#SUBTITLETRANSLIT":   self.subtitleTranslit = s[1].strip()[:-1]
            elif s[0] == "#ARTISTTRANSLIT":     self.artistTranslit = s[1].strip()[:-1]
            elif s[0] == "#GENRE":              self.genre = s[1].strip()[:-1]
            elif s[0] == "#CREDIT":             self.credit = s[1].strip()[:-1]
            elif s[0] == "#BANNER":             self.banner = s[1].strip()[:-1]
            elif s[0] == "#BACKGROUND":         self.background = s[1].strip()[:-1]
            elif s[0] == "#LYRICSPATH":         self.lyricsPath = s[1].strip()[:-1]
            elif s[0] == "#CDTITLE":            self.cdTitle = s[1].strip()[:-1]
            elif s[0] == "#MUSIC":              self.music = s[1].strip()[:-1]
            elif s[0] == "#OFFSET":             self.offset = float(s[1].strip()[:-1])
            elif s[0] == "#BPMS":               self._readBpms(s[1].strip().split(",")[:-1])
            elif s[0] == "#STOPS":              self._readStops(s[1].strip().split(",")[:-1][:-1])
            elif s[0] == "#SAMPLESTART":        self.sampleStart = float(s[1].strip()[:-1])
            elif s[0] == "#SAMPLELENGTH":       self.sampleLength = float(s[1].strip()[:-1])
            elif s[0] == "#DISPLAYBPM":         self.displayBpm = s[1].strip()[:-1]
            elif s[0] == "#SELECTABLE":         self.selectable = True if s[1].strip()[:-1] == "YES" else False
            elif s[0] == "#BGCHANGES":          self.bgChanges = s[1].strip()[:-1]
            elif s[0] == "#FGCHANGES":          self.fgChanges = s[1].strip()[:-1]

    def _readNoteMetadata(self, lines: List[str]):
        self.chartType = lines[0].strip()[:-1]
        self.description = lines[1].strip()[:-1]
        self.difficulty = lines[2].strip()[:-1]
        self.difficultyVal = int(lines[3].strip()[:-1])
        self.grooveRadar = [float(x) for x in lines[4].strip()[:-1].split(",")]

    def _readNotes(self, lines: List[str]):

        pass

    def _readBpms(self, lines: List[str]):
        pass

    def _readStops(self, lines: List[str]):
        pass


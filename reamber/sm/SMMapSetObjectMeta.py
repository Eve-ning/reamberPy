from reamber.sm.SMBpmObject import SMBpmObject
from reamber.sm.SMStopObject import SMStopObject

from reamber.base.BpmObject import BpmObject

from reamber.base.RAConst import RAConst

from dataclasses import dataclass
from dataclasses import field
from typing import List


@dataclass
class SMMapSetObjectMeta:
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
    offset: float = None  # Offset is None as we do a comparison on offset, see SMMapSetObject.py::_readBpms
    _bpmsStr: List[str] = field(default_factory=lambda: [])
    _stopsStr: List[str] = field(default_factory=lambda: [])
    stops: List[SMStopObject] = field(default_factory=lambda: [])
    sampleStart: float = 0.0
    sampleLength: float = 10.0
    displayBpm: str = ""
    selectable: bool = True
    bgChanges: str = ""  # Idk what this does
    fgChanges: str = ""  # Idk what this does

    def _readMetadata(self, lines: List[str]):
        for line in lines:
            if line == "":
                continue

            s = [token.strip() for token in line.split(":")]

            if   s[0] == "#TITLE":              self.title = s[1].strip()
            elif s[0] == "#SUBTITLE":           self.subtitle = s[1].strip()
            elif s[0] == "#ARTIST":             self.artist = s[1].strip()
            elif s[0] == "#TITLETRANSLIT":      self.titleTranslit = s[1].strip()
            elif s[0] == "#SUBTITLETRANSLIT":   self.subtitleTranslit = s[1].strip()
            elif s[0] == "#ARTISTTRANSLIT":     self.artistTranslit = s[1].strip()
            elif s[0] == "#GENRE":              self.genre = s[1].strip()
            elif s[0] == "#CREDIT":             self.credit = s[1].strip()
            elif s[0] == "#BANNER":             self.banner = s[1].strip()
            elif s[0] == "#BACKGROUND":         self.background = s[1].strip()
            elif s[0] == "#LYRICSPATH":         self.lyricsPath = s[1].strip()
            elif s[0] == "#CDTITLE":            self.cdTitle = s[1].strip()
            elif s[0] == "#MUSIC":              self.music = s[1].strip()
            elif s[0] == "#OFFSET":             self.offset = RAConst.secToMSec(float(s[1].strip()))
            elif s[0] == "#BPMS":               self._bpmsStr = s[1].strip().split(",")
            elif s[0] == "#STOPS":              self._stopsStr = s[1].strip().split(",")
            elif s[0] == "#SAMPLESTART":        self.sampleStart = RAConst.secToMSec(float(s[1].strip()))
            elif s[0] == "#SAMPLELENGTH":       self.sampleLength = RAConst.secToMSec(float(s[1].strip()))
            elif s[0] == "#DISPLAYBpm":         self.displayBpm = s[1].strip()
            elif s[0] == "#SELECTABLE":         self.selectable = True if s[1].strip() == "YES" else False
            elif s[0] == "#BGCHANGES":          self.bgChanges = s[1].strip()
            elif s[0] == "#FGCHANGES":          self.fgChanges = s[1].strip()

    def _writeMetadata(self, bpms: List[BpmObject]) -> List[str]:
        bpms.sort(key=lambda tp: tp.offset)

        bpmBeats = SMBpmObject.getBeats(bpms, bpms)
        stopBeats = SMBpmObject.getBeats(self.stops, bpms)

        return [
            f"#TITLE:{self.title};",
            f"#SUBTITLE:{self.subtitle};",
            f"#ARTIST:{self.artist};",
            f"#TITLETRANSLIT:{self.titleTranslit};",
            f"#SUBTITLETRANSLIT:{self.subtitleTranslit};",
            f"#ARTISTTRANSLIT:{self.artistTranslit};",
            f"#GENRE:{self.genre};",
            f"#CREDIT:{self.credit};",
            f"#BANNER:{self.banner};",
            f"#BACKGROUND:{self.background};",
            f"#LYRICSPATH:{self.lyricsPath};",
            f"#CDTITLE:{self.cdTitle};",
            f"#MUSIC:{self.music};",
            f"#OFFSET:{RAConst.mSecToSec(self.offset)};",
            f"#BPMS:" + ",\n".join([f"{beat}={bpm.bpm}" for beat, bpm in zip(bpmBeats, bpms)]) + ";",
            f"#STOPS:" + ",\n".join([f"{beat}={RAConst.mSecToSec(stop.length)}" for
                                     beat, stop in zip(stopBeats, self.stops)]) + ";",
            f"#SAMPLESTART:{RAConst.mSecToSec(self.sampleStart)};",
            f"#SAMPLELENGTH:{RAConst.mSecToSec(self.sampleLength)};",
            f"#DISPLAYBpm:{self.displayBpm};",
            f"#SELECTABLE:" + "YES;" if self.selectable else "NO;",
            f"#BGCHANGES:{self.bgChanges};",
            f"#FGCHANGES:{self.fgChanges};",
        ]

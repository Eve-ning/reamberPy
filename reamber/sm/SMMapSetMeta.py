from dataclasses import dataclass
from dataclasses import field
from typing import List

from reamber.base.Bpm import Bpm
from reamber.base.RAConst import RAConst
from reamber.sm.SMBpm import SMBpm
from reamber.sm.SMStop import SMStop


@dataclass
class SMMapSetMeta:
    title:            str = ""
    subtitle:         str = ""
    artist:           str = ""
    title_translit:   str = ""
    subtitle_translit: str = ""
    artist_translit:  str = ""
    genre:            str = ""
    credit:           str = ""
    banner:           str = ""
    background:       str = ""
    lyrics_path:       str = ""
    cd_title:          str = ""
    music:            str = ""
    offset:           float = None  # Offset is None as we do a comparison on offset, see SMMapSet.py::_readBpms
    _bpmsStr:         List[str] = field(default_factory=lambda: [])
    _stopsStr:        List[str] = field(default_factory=lambda: [])
    stops:            List[SMStop] = field(default_factory=lambda: [])
    sample_start:     float = 0.0
    sample_length:    float = 10.0
    display_bpm:       str = ""
    selectable:       bool = True
    bg_changes:        str = ""  # Idk what this does
    fg_changes:        str = ""  # Idk what this does

    def _read_metadata(self, lines: List[str]):
        for line in lines:
            if line == "":
                continue

            s = [token.strip() for token in line.split(":")]
            # This is to get rid of comments
            # e.g.
            # // HELLO\n#TITLE:WORLD -> #TITLE:WORLD
            if len(s[0]) == 0: continue
            if not s[0].startswith("#"): s[0] = s[0][s[0].rfind('#'):]

            if   s[0] == "#TITLE":              self.title = s[1].strip()
            elif s[0] == "#SUBTITLE":           self.subtitle = s[1].strip()
            elif s[0] == "#ARTIST":             self.artist = s[1].strip()
            elif s[0] == "#TITLETRANSLIT":      self.title_translit = s[1].strip()
            elif s[0] == "#SUBTITLETRANSLIT":   self.subtitle_translit = s[1].strip()
            elif s[0] == "#ARTISTTRANSLIT":     self.artist_translit = s[1].strip()
            elif s[0] == "#GENRE":              self.genre = s[1].strip()
            elif s[0] == "#CREDIT":             self.credit = s[1].strip()
            elif s[0] == "#BANNER":             self.banner = s[1].strip()
            elif s[0] == "#BACKGROUND":         self.background = s[1].strip()
            elif s[0] == "#LYRICSPATH":         self.lyrics_path = s[1].strip()
            elif s[0] == "#CDTITLE":            self.cd_title = s[1].strip()
            elif s[0] == "#MUSIC":              self.music = s[1].strip()
            elif s[0] == "#OFFSET":             self.offset = RAConst.sec_to_msec(float(s[1].strip()))
            elif s[0] == "#BPMS":               self._bpmsStr = s[1].strip().split(",")
            elif s[0] == "#STOPS":              self._stopsStr = s[1].strip().split(",")
            elif s[0] == "#SAMPLESTART":        self.sample_start = RAConst.sec_to_msec(float(s[1].strip()))
            elif s[0] == "#SAMPLELENGTH":       self.sample_length = RAConst.sec_to_msec(float(s[1].strip()))
            elif s[0] == "#DISPLAYBpm":         self.display_bpm = s[1].strip()
            elif s[0] == "#SELECTABLE":         self.selectable = True if s[1].strip() == "YES" else False
            elif s[0] == "#BGCHANGES":          self.bg_changes = s[1].strip()
            elif s[0] == "#FGCHANGES":          self.fg_changes = s[1].strip()

    def _write_metadata(self, bpm: List[Bpm]) -> List[str]:
        bpms.sort()

        bpm_beats = SMBpm.get_beats(bpms, bpms)
        stop_beats = SMBpm.get_beats(self.stops, bpms)

        return [
            f"#TITLE:{self.title};",
            f"#SUBTITLE:{self.subtitle};",
            f"#ARTIST:{self.artist};",
            f"#TITLETRANSLIT:{self.title_translit};",
            f"#SUBTITLETRANSLIT:{self.subtitle_translit};",
            f"#ARTISTTRANSLIT:{self.artist_translit};",
            f"#GENRE:{self.genre};",
            f"#CREDIT:{self.credit};",
            f"#BANNER:{self.banner};",
            f"#BACKGROUND:{self.background};",
            f"#LYRICSPATH:{self.lyrics_path};",
            f"#CDTITLE:{self.cd_title};",
            f"#MUSIC:{self.music};",
            f"#OFFSET:{RAConst.msec_to_sec(self.offset)};",
            f"#BPMS:" + ",\n".join([f"{beat}={bpm.bpm}" for beat, bpm in zip(bpm_beats, bpms)]) + ";",
            f"#STOPS:" + ",\n".join([f"{beat}={RAConst.msec_to_sec(stop.length)}" for
                                     beat, stop in zip(stop_beats, self.stops)]) + ";",
            f"#SAMPLESTART:{RAConst.msec_to_sec(self.sample_start)};",
            f"#SAMPLELENGTH:{RAConst.msec_to_sec(self.sample_length)};",
            f"#DISPLAYBpm:{self.display_bpm};",
            f"#SELECTABLE:" + "YES;" if self.selectable else "NO;",
            f"#BGCHANGES:{self.bg_changes};",
            f"#FGCHANGES:{self.fg_changes};",
        ]

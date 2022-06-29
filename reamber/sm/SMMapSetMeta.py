from dataclasses import dataclass
from typing import List, TYPE_CHECKING

from reamber.algorithms.timing.TimingMap import TimingMap
from reamber.algorithms.timing.utils.BpmChangeSnap import BpmChangeSnap
from reamber.algorithms.timing.utils.snap import Snap
from reamber.base.RAConst import RAConst
from reamber.sm.SMBpm import SMBpm
from reamber.sm.SMStop import SMStop
from reamber.sm.lists.SMBpmList import SMBpmList
from reamber.sm.lists.SMStopList import SMStopList

if TYPE_CHECKING:
    from reamber.sm.SMMapSet import SMMapSet


@dataclass
class SMMapSetMeta:
    title: str = ""
    subtitle: str = ""
    artist: str = ""
    title_translit: str = ""
    subtitle_translit: str = ""
    artist_translit: str = ""
    genre: str = ""
    credit: str = ""
    banner: str = ""
    background: str = ""
    lyrics_path: str = ""
    cd_title: str = ""
    music: str = ""
    # Offset is None to compare offset, see SMMapSet.py::_read_bpms
    offset: float = None
    sample_start: float = 0.0
    sample_length: float = 10.0
    display_bpm: str = ""
    selectable: bool = True
    bg_changes: str = ""  # Idk what this does
    fg_changes: str = ""  # Idk what this does

    def _read_metadata(self: "SMMapSet", lines: List[str]):
        bpms, stops = None, None
        for line in lines:
            if line == "": continue

            s = [token.strip() for token in line.split(":")]
            # This is to get rid of comments
            # e.g.
            # // HELLO\n#TITLE:WORLD -> #TITLE:WORLD
            if len(s[0]) == 0: continue
            if not s[0].startswith("#"): s[0] = s[0][s[0].rfind('#'):]

            if s[0] == "#TITLE":
                self.title = s[1].strip()
            elif s[0] == "#SUBTITLE":
                self.subtitle = s[1].strip()
            elif s[0] == "#ARTIST":
                self.artist = s[1].strip()
            elif s[0] == "#TITLETRANSLIT":
                self.title_translit = s[1].strip()
            elif s[0] == "#SUBTITLETRANSLIT":
                self.subtitle_translit = s[1].strip()
            elif s[0] == "#ARTISTTRANSLIT":
                self.artist_translit = s[1].strip()
            elif s[0] == "#GENRE":
                self.genre = s[1].strip()
            elif s[0] == "#CREDIT":
                self.credit = s[1].strip()
            elif s[0] == "#BANNER":
                self.banner = s[1].strip()
            elif s[0] == "#BACKGROUND":
                self.background = s[1].strip()
            elif s[0] == "#LYRICSPATH":
                self.lyrics_path = s[1].strip()
            elif s[0] == "#CDTITLE":
                self.cd_title = s[1].strip()
            elif s[0] == "#MUSIC":
                self.music = s[1].strip()
            elif s[0] == "#OFFSET":
                self.offset = RAConst.sec_to_msec(float(s[1].strip()))
            elif s[0] == "#BPMS":
                bpms = self._read_bpms(self.offset, s[1].strip().split(","))
            elif s[0] == "#STOPS":
                stops = self._read_stops(bpms, s[1].strip().split(","))
            elif s[0] == "#SAMPLESTART":
                self.sample_start = RAConst.sec_to_msec(float(s[1].strip()))
            elif s[0] == "#SAMPLELENGTH":
                self.sample_length = RAConst.sec_to_msec(float(s[1].strip()))
            elif s[0] == "#DISPLAYBPM":
                self.display_bpm = s[1].strip()
            elif s[0] == "#SELECTABLE":
                self.selectable = True if s[1].strip() == "YES" else False
            elif s[0] == "#BGCHANGES":
                self.bg_changes = s[1].strip()
            elif s[0] == "#FGCHANGES":
                self.fg_changes = s[1].strip()

        return bpms, stops

    @staticmethod
    def _read_bpms(offset: float, lines: List[str]) -> SMBpmList:
        assert offset is not None, "Offset should be defined BEFORE Bpm"

        bcs_s = []
        for line in lines:
            beat, bpm = map(float, line.split('='))
            bcs_s.append(BpmChangeSnap(bpm, 4, Snap(0, beat, 4)))

        tm = TimingMap.from_bpm_changes_snap(offset, bcs_s)
        return SMBpmList(
            [SMBpm(b.offset, b.bpm) for b in tm.bpm_changes_offset]
        )

    @staticmethod
    def _read_stops(bpms: SMBpmList, lines: List[str]):
        tm = bpms.to_timing_map()

        if not lines: return SMStopList([])
        stops = []
        for line in lines:
            beat, length = map(float, line.split('='))
            stops.append(SMStop(
                tm.offsets([Snap(0, beat, 4)])[0],
                RAConst.sec_to_msec(length)
            ))
        return stops

    def _write_metadata(self: 'SMMapSet') -> List[str]:
        tm = self[0].bpms.to_timing_map()
        bpm_beats = tm.beats(self[0].bpms.offset)
        stop_beats = tm.beats(self[0].stops.offset)

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
            f"#BPMS:" + ",\n".join(
                [f"{round(float(beat), 2)}={bpm.bpm}" for beat, bpm in
                 zip(bpm_beats, self[0].bpms)]) + ";",
            f"#STOPS:" + ",\n".join(
                [f"{round(float(beat), 2)}={RAConst.msec_to_sec(stop.length)}"
                 for beat, stop in zip(stop_beats, self[0].stops)]) + ";",
            f"#SAMPLESTART:{RAConst.msec_to_sec(self.sample_start)};",
            f"#SAMPLELENGTH:{RAConst.msec_to_sec(self.sample_length)};",
            f"#DISPLAYBPM:{self.display_bpm};",
            f"#SELECTABLE:" + "YES;" if self.selectable else "NO;",
            f"#BGCHANGES:{self.bg_changes};",
            f"#FGCHANGES:{self.fg_changes};",
        ]

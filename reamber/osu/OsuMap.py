from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from reamber.base.Map import Map
from reamber.base.Property import map_props, stack_props
from reamber.base.lists import TimedList
from reamber.osu.OsuMapMeta import OsuMapMeta
from reamber.osu.OsuNoteMeta import OsuNoteMeta
from reamber.osu.OsuTimingPointMeta import OsuTimingPointMeta
from reamber.osu.lists.OsuBpmList import OsuBpmList
from reamber.osu.lists.OsuSampleList import OsuSampleList
from reamber.osu.lists.OsuSvList import OsuSvList
from reamber.osu.lists.notes.OsuHitList import OsuHitList
from reamber.osu.lists.notes.OsuHoldList import OsuHoldList
from reamber.osu.lists.notes.OsuNoteList import OsuNoteList


@map_props()
@dataclass
class OsuMap(Map[OsuNoteList, OsuHitList, OsuHoldList, OsuBpmList],
             OsuMapMeta):
    _props = dict(svs=OsuSvList)
    objs: dict[str, TimedList] = \
        field(init=False,
              default_factory=lambda: dict(svs=OsuSvList([]),
                                           hits=OsuHitList([]),
                                           holds=OsuHoldList([]),
                                           bpms=OsuBpmList([])))

    def reset_samples(self, of_notes=True, of_samples=True) -> None:
        """Resets all hitsounds and samples"""
        if of_notes:
            for n in self.hits: n.reset_samples()
            for n in self.holds: n.reset_samples()

        if of_samples: self.samples = OsuSampleList([])

    @staticmethod
    def read(lines: list[str]) -> OsuMap:
        """Reads a .osu file string list as an OsuMap 
        
        See Also:
            read_file: To read from a .osu file
        """

        m = OsuMap()
        lines = [line.strip() for line in lines]  # Redundancy for safety

        try:
            ix_tp = lines.index("[TimingPoints]")
            ix_ho = lines.index("[HitObjects]")
        except ValueError:
            raise Exception("Bad File Format. "
                            "No [TimingPoints] & [HitObjects].")

        m._read_file_metadata(lines[:ix_tp])
        m._read_file_timing_points(lines[ix_tp + 1:ix_ho])
        m._read_file_hit_objects(lines[ix_ho + 1:])

        return m

    @staticmethod
    def read_file(file_path: str | Path) -> OsuMap:
        """Reads a .osu file"""

        with open(Path(file_path).as_posix(), "r", encoding="utf8") as f:
            lines = f.read().split("\n")

        return OsuMap.read(lines=lines)

    def write_file(self, file_path: str | Path):
        """Writes a .osu file"""

        with open(Path(file_path).as_posix(), "w+", encoding="utf8") as f:
            f.writelines("\n".join(self.write()))

    def write(self) -> list[str]:
        """Writes a list of strings for .osu format. """

        lines = []

        lines.extend(self.write_meta_string_list())

        lines.append("\n[TimingPoints]")
        lines.extend([b.write_string() for b in self.bpms])
        lines.extend([b.write_string() for b in self.svs])
        lines.append("\n\n[HitObjects]")
        for obj in sorted([*self.holds, *self.hits], key=lambda x: x.offset):
            lines.append(obj.write_string(keys=int(self.circle_size)))

        return lines

    def _read_file_metadata(self, lines: list[str]):
        """Reads the metadata only, inclusive of Events"""
        self._read_meta_string_list(lines)

    def _read_file_timing_points(self, lines: list[str]):
        """Reads all TimingPoints"""
        self.svs = OsuSvList.read(
            [i for i in lines if OsuTimingPointMeta.is_slider_velocity(i)])
        self.bpms = OsuBpmList.read(
            [i for i in lines if OsuTimingPointMeta.is_timing_point(i)])

    def _read_file_hit_objects(self, lines: list[str]):
        """Reads all HitObjects"""
        k = int(self.circle_size)
        self.hits = OsuHitList.read(
            [i for i in lines if OsuNoteMeta.is_hit(i)], k)
        self.holds = OsuHoldList.read(
            [i for i in lines if OsuNoteMeta.is_hold(i)], k)

    # noinspection PyMethodOverriding
    def metadata(self, unicode=True) -> str:
        """Grabs the map metadata

        Args:
            unicode: Returns the unicode version if available
        """
        fmt = "{} - {}, {} ({})"

        if unicode:
            return fmt.format(self.artist_unicode, self.title_unicode,
                              self.version, self.creator)
        else:
            return fmt.format(self.artist, self.title,
                              self.version, self.creator)

    def rate(self, by: float):
        """Changes the rate of the map"""
        osu = super(OsuMap, self.deepcopy()).rate(by)
        osu.samples.offset /= by
        osu.preview_time /= by

        return osu

    @stack_props()
    class Stacker(Map.Stacker):
        _props = ["hitsound_set", "sample_set", "sample_set_index",
                  "addition_set", "custom_set", "volume",
                  "hitsound_file", "kiai"]

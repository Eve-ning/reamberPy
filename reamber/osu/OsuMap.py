from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Union

from reamber.base.Map import Map
from reamber.base.Property import map_props, stack_props
from reamber.base.lists import TimedList
from reamber.osu.OsuBpm import OsuBpm
from reamber.osu.OsuMapMeta import OsuMapMeta
from reamber.osu.OsuNoteMeta import OsuNoteMeta
from reamber.osu.OsuSv import OsuSv
from reamber.osu.OsuTimingPointMeta import OsuTimingPointMeta
from reamber.osu.lists.OsuBpmList import OsuBpmList
from reamber.osu.lists.OsuSampleList import OsuSampleList
from reamber.osu.lists.OsuSvList import OsuSvList
from reamber.osu.lists.notes.OsuHitList import OsuHitList
from reamber.osu.lists.notes.OsuHoldList import OsuHoldList
from reamber.osu.lists.notes.OsuNoteList import OsuNoteList

@map_props()
@dataclass
class OsuMap(Map[OsuNoteList, OsuHitList, OsuHoldList, OsuBpmList], OsuMapMeta):

    _props = dict(svs=OsuSvList)
    objs: Dict[str, TimedList] = \
        field(init=False,
              default_factory=lambda: dict(svs=OsuSvList([]),
                                           hits=OsuHitList([]),
                                           holds=OsuHoldList([]),
                                           bpms=OsuBpmList([])))

    def reset_all_samples(self, notes=True, samples=True) -> None:
        """ Resets all hitsounds and samples

        :param notes: Whether to reset hitsounds on notes
        :param samples: Whether to reset samples
        """
        if notes:
            for n in self.hits: n.reset_samples()
            for n in self.holds: n.reset_samples()

        if samples: self.samples = OsuSampleList([])

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

        self._read_file_metadata(lines[:ix_tp])
        self._read_file_timing_points(lines[ix_tp + 1:ix_ho])
        self._read_file_hit_objects(lines[ix_ho + 1:])

        return self

    @staticmethod
    def read_file(file_path: str) -> OsuMap:
        """ Reads a .osu, loads inplace, hence it doesn't return anything

        :param file_path: The path to the .osu file."""

        with open(file_path, "r", encoding="utf8") as f:
            # We read the file and firstly find the distinct sections
            # 1) Meta 2) Timing Points 3) Hit Objects

            file = [i.strip() for i in f.read().split("\n")]

        return OsuMap.read(lines=file)

    def write_file(self, file_path=""):
        """ Writes a .osu, doesn't return anything.

        :param file_path: The path to a new .osu file."""

        with open(file_path, "w+", encoding="utf8") as f:
            f.writelines("\n".join(self.write()))

    def write(self) -> List[str]:
        """ Writes a list of strings, compatible with .osu file. """

        out = []

        for s in self.write_meta_string_list():
            out.append(s)

        out.append("\n[TimingPoints]")
        for tp in self.bpms:
            assert isinstance(tp, OsuBpm)
            out.append(tp.write_string())

        for tp in self.svs:
            assert isinstance(tp, OsuSv)
            out.append(tp.write_string())

        out.append("[HitObjects]")
        for obj in sorted([*self.holds, *self.hits], key=lambda x: x.offset):
            out.append(obj.write_string(keys=int(self.circle_size)))

        return out

    def _read_file_metadata(self, lines: List[str]):
        """ Reads the metadata only, inclusive of Events """
        self._read_meta_string_list(lines)

    def _read_file_timing_points(self, lines: Union[List[str], str]):
        """ Reads all TimingPoints """
        lines = lines if isinstance(lines, list) else [lines]
        self.svs = OsuSvList.read([li for li in lines if OsuTimingPointMeta.is_slider_velocity(li)])
        self.bpms = OsuBpmList.read([li for li in lines if OsuTimingPointMeta.is_timing_point(li)])

    def _read_file_hit_objects(self, lines: Union[List[str], str]):
        """ Reads all HitObjects """
        lines = lines if isinstance(lines, list) else [lines]
        k = int(self.circle_size)
        self.hits = OsuHitList.read([li for li in lines if OsuNoteMeta.is_hit(li)], k)
        self.holds = OsuHoldList.read([li for li in lines if OsuNoteMeta.is_hold(li)], k)

    # noinspection DuplicatedCode
    def scroll_speed(self, center_bpm: float = None) -> List[Dict[str, float]]:
        """ Evaluates the scroll speed based on mapType. Overrides the base to include SV
    
        e.g. if BPM == 200.0 and CenterBPM == 100.0, it'll return {'offset': X, 'speed': 2.0}

        :param center_bpm: The bpm to zero calculations on. If None, it'll just be the multiplication of bpm and sv.
        :return: Returns a list dict of keys offset and speed
        """
    
        # This automatically calculates the center BPM
        # Bpm Activity implicitly sorts
        if center_bpm is None: center_bpm = 1
    
        sv_pairs = [(offset, multiplier) for offset, multiplier in zip(self.svs.sorted().offset, self.svs.multiplier)]
        bpm_pairs = [(offset, bpm) for offset, bpm in zip(self.bpms.offset, self.bpms.bpm)]
    
        curr_bpm_iter = 0
        next_bpm_offset = None if len(bpm_pairs) == 1 else bpm_pairs[1][0]
        speed_list = []
    
        for offset, sv in sv_pairs:
            while offset < bpm_pairs[0][0]:  # Offset cannot be less than the first bpm
                continue
            # Guarantee that svOffset is after first bpm
            if next_bpm_offset and offset >= next_bpm_offset:
                curr_bpm_iter += 1
                if curr_bpm_iter != len(bpm_pairs):
                    next_bpm_offset = bpm_pairs[curr_bpm_iter][0]
                else:
                    next_bpm_offset = None
            speed_list.append(dict(offset=offset, speed=bpm_pairs[curr_bpm_iter][1] * sv / center_bpm))
    
        return speed_list

    # noinspection PyMethodOverriding
    def metadata(self, unicode=True) -> str:
        """ Grabs the map metadata

        :param unicode: Whether to try to find the unicode or non-unicode. \
            This doesn't try to convert unicode to ascii, it just looks for if there's an available translation.
        :return:
        """

        def formatting(artist, title, difficulty, creator):
            return f"{artist} - {title}, {difficulty} ({creator})"

        if unicode: return formatting(self.artist_unicode, self.title_unicode, self.version, self.creator)
        else: return formatting(self.artist, self.title, self.version, self.creator)

    def rate(self, by: float):
        """ Changes the rate of the map

        :param by: The value to rate it by. 1.1x speeds up the song by 10%. Hence 10/11 of the length.
        """
        osu = super(OsuMap, self.deepcopy()).rate(by=by)
        osu.samples.offset /= by
        osu.preview_time /= by

        return osu

    @stack_props()
    class Stacker(Map.Stacker):
        _props = ["hitsound_set",  "sample_set", "sample_set_index",
                  "addition_set", "custom_set", "volume",
                  "hitsound_file", "kiai"]


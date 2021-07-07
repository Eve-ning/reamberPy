from __future__ import annotations

from ctypes import Union
from dataclasses import dataclass, field
from typing import List

from reamber.base.MapSet import MapSet
from reamber.base.RAConst import RAConst
from reamber.sm.SMBpm import SMBpm
from reamber.sm.SMMap import SMMap
from reamber.sm.SMMapSetMeta import SMMapSetMeta
from reamber.sm.SMStop import SMStop
from reamber.sm.lists.SMBpmList import SMBpmList


@dataclass
class SMMapSet(SMMapSetMeta, MapSet):

    maps: List[SMMap] = field(default_factory=lambda: [])

    @staticmethod
    def read(lines: Union[str, List[str]]) -> SMMapSet:
        """ Reads a .sm file

        It reads all .sm as a mapset due to the nature of the file format.

        Note that it's best to just pass the .read as the argument.
        This uses a very specific splitting, not \\n.

        :param lines: The lines to the file.
        """
        self = SMMapSet()
        lines = "\n".join(lines) if isinstance(lines, list) else lines
        file_spl = [i.strip() for i in lines.split(";")]
        metadata = []
        maps = []
        for token in file_spl:
            if "#NOTES:" in token:
                maps.append(token)
            else:
                metadata.append(token)

        self._read_metadata(metadata)
        bpms = self._read_bpms(offset=self.offset, lines=self._bpmsStr)
        self._read_stops(lines=self._stopsStr, bpms=bpms)
        self._read_maps(maps=maps, bpms=bpms, stops=self.stops)

        for map in self.maps:
            map.bpms = bpms

        return self

    @staticmethod
    def read_file(file_path: str) -> SMMapSet:
        """ Reads a .sm file

        It reads all .sm as a mapset due to the nature of the file format.

        :param file_path: The path to the file
        """
        with open(file_path, "r", encoding="utf8") as f:
            file = f.read()

        # noinspection PyTypeChecker
        return SMMapSet.read(file)

    def write_file(self, file_path: str,
                   align_bpms: bool = False,
                   BEAT_CORRECTION_FACTOR=5.0,
                   BEAT_ERROR_THRESHOLD=0.001):
        """ Writes the file to file_path specified

        :param BEAT_ERROR_THRESHOLD: See Bpm.py::alignBpms for details
        :param BEAT_CORRECTION_FACTOR: See Bpm.py::alignBpms for details
        :param file_path: File Path
        :param align_bpms: Aligns the BPM by mutating the current file. Details in Bpm.py
        """
        with open(file_path, "w+", encoding="utf8") as f:
            if align_bpms:
                for map in self.maps:
                    map.bpms = SMBpm.align_bpms(map.bpms,
                                                BEAT_CORRECTION_FACTOR=BEAT_CORRECTION_FACTOR,
                                                BEAT_ERROR_THRESHOLD=BEAT_ERROR_THRESHOLD)
            for s in self._write_metadata(self.maps[0].bpms):
                f.write(s + "\n")

            for map in self.maps:
                assert isinstance(map, SMMap)
                for s in map.write_string():
                    f.write(s + "\n")

    @staticmethod
    def _read_bpms(offset: float, lines: List[str]) -> SMBpmList:
        assert offset is not None, "Offset should be defined BEFORE Bpm"
        bpms = []
        beat_prev = 0.0
        bpm_prev = 1.0
        for line in lines:
            beat_curr, bpm_curr = [float(x.strip()) for x in line.split("=")]
            offset += (beat_curr - beat_prev) * RAConst.min_to_msec(1.0 / bpm_prev)
            bpms.append(SMBpm(offset=offset, bpm=bpm_curr))
            beat_prev = beat_curr
            bpm_prev = bpm_curr

        return SMBpmList(bpms)

    def _read_stops(self, bpms: List[SMBpm], lines: List[str]):
        for line in lines:
            if len(line) == 0: return
            beat_curr, length_curr = [float(x.strip()) for x in line.split("=")]

            index = 0
            for index, bpm in enumerate(bpms):
                if bpm.beat(bpms) > beat_curr:
                    index -= 1
                    break

            offset = bpms[index].offset + (beat_curr - bpms[index].beat(bpms)) * bpms[index].beat_length()

            self.stops.append(SMStop(offset=offset, length=RAConst.sec_to_msec(length_curr)))

    def _read_maps(self, maps: List[str], bpms: List[SMBpm], stops: List[SMStop]):
        for map in maps:
            self.maps.append(SMMap.read_string(note_str=map, bpms=bpms, stops=stops))

    def rate(self, by: float, inplace:bool = False):
        """ Changes the rate of the map

        :param by: The value to rate it by. 1.1x speeds up the song by 10%. Hence 10/11 of the length.
        :param inplace: Whether to perform the operation in place. Returns a copy if False
        """
        this = self if inplace else self.deepcopy()
        super(SMMapSet, this).rate(by=by, inplace=True)

        # We invert it so it's easier to cast on Mult
        by = 1 / by
        this.sample_start *= by
        this.sample_length *= by

        return None if inplace else this

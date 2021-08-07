from __future__ import annotations

from ctypes import Union
from dataclasses import dataclass
from typing import List

from reamber.base.MapSet import MapSet
from reamber.sm.SMMap import SMMap
from reamber.sm.SMMapSetMeta import SMMapSetMeta
from reamber.sm.SMStop import SMStop
from reamber.sm.lists import SMStopList
from reamber.sm.lists.SMBpmList import SMBpmList
from reamber.sm.lists.notes import SMNoteList, SMHitList, SMHoldList


@dataclass
class SMMapSet(MapSet[SMNoteList, SMHitList, SMHoldList, SMBpmList, SMMap], SMMapSetMeta):

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

        bpms, stops = self._read_metadata(metadata)
        self._read_maps(maps=maps, bpms=bpms, stops=stops)

        bpms = bpms.reseat()  # Force Reseats the metronome to 4
        for m in self.maps:
            m.bpms = bpms
            m.stops = SMStopList([])
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

    def write_file(self, file_path: str):
        """ Writes the file to file_path specified

        :param file_path: File Path
        """
        with open(file_path, "w+", encoding="utf8") as f:
            for s in self._write_metadata():
                f.write(s + "\n")

            for map in self.maps:
                assert isinstance(map, SMMap)
                for s in map.write_string():
                    f.write(s + "\n")

    def _read_maps(self, maps: List[str], bpms: SMBpmList, stops: List[SMStop]):
        self.maps = [SMMap.read_string(note_str=map, bpms=bpms, stops=stops) for map in maps]

    # noinspection PyTypeChecker
    def rate(self, by: float):
        """ Changes the rate of the map

        :param by: The value to rate it by. 1.1x speeds up the song by 10%. Hence 10/11 of the length.
        """
        sms = super().rate(by=by)
        sms: SMMapSet
        sms.sample_start /= by
        sms.sample_length /= by

        return sms

    class Stacker(MapSet.Stacker):
        ...


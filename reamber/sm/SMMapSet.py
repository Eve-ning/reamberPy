from __future__ import annotations

from dataclasses import dataclass
from typing import List

from reamber.algorithms.timing.utils.BpmChangeSnap import BpmChangeSnap
from reamber.base.MapSet import MapSet
from reamber.sm.SMMap import SMMap
from reamber.sm.SMMapSetMeta import SMMapSetMeta
from reamber.sm.lists import SMStopList
from reamber.sm.lists.SMBpmList import SMBpmList
from reamber.sm.lists.notes import SMNoteList, SMHitList, SMHoldList


@dataclass
class SMMapSet(MapSet[SMNoteList, SMHitList, SMHoldList, SMBpmList, SMMap],
               SMMapSetMeta):

    @staticmethod
    def read(lines: str | list[str]) -> SMMapSet:
        """Reads a .sm file"""
        ms = SMMapSet()
        lines = "\n".join(lines) if isinstance(lines, list) else lines
        file_spl = [i.strip() for i in lines.split(";")]
        metadata = []
        maps = []
        for token in file_spl:
            if "#NOTES:" in token:
                maps.append(token)
            else:
                metadata.append(token)

        bcs_s, stops = ms._read_metadata(metadata)
        ms._read_maps(maps=maps, bcs_s=bcs_s, stops=stops)
        return ms

    @staticmethod
    def read_file(file_path: str) -> SMMapSet:
        """Reads a .sm file as a Mapset"""
        with open(file_path, "r", encoding="utf8") as f:
            file = f.read()

        return SMMapSet.read(file)

    def write(self) -> str:
        """Writes as a list[str] """
        m = self._write_metadata()

        for map in self.maps:
            m.extend(map.write())
        return "\n".join(m)

    def write_file(self, file_path: str):
        """Writes the file to file_path specified"""
        with open(file_path, "w+", encoding="utf8") as f:
            f.write(self.write())

    def _read_maps(self,
                   maps: List[str],
                   bcs_s: List[BpmChangeSnap],
                   stops: SMStopList):
        self.maps = [
            SMMap.read(s=map_str, bcs_s=bcs_s, stops=stops,
                       initial_offset=self.offset)
            for map_str in maps
        ]

    def rate(self, by: float) -> SMMapSet:
        """Changes the rate of the map"""
        sms = super(SMMapSet, self).rate(by=by)
        sms.sample_start /= by
        sms.sample_length /= by

        return sms

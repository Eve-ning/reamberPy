from __future__ import annotations

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
class SMMapSet(MapSet[SMNoteList, SMHitList, SMHoldList, SMBpmList, SMMap],
               SMMapSetMeta):

    @staticmethod
    def read(lines: str | list[str]) -> SMMapSet:
        """ Reads a .sm file """
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

        bpms, stops = ms._read_metadata(metadata)
        ms._read_maps(maps=maps, bpms=bpms, stops=stops)

        bpms = bpms.reseat()  # Force Reseats the metronome to 4
        for m in ms.maps:
            m.bpms = bpms
            m.stops = SMStopList([])
        return ms

    @staticmethod
    def read_file(file_path: str) -> SMMapSet:
        """ Reads a .sm file as a Mapset """
        with open(file_path, "r", encoding="utf8") as f:
            file = f.read()

        return SMMapSet.read(file)

    def write(self) -> list[str]:
        """ Writes as a list[str] """
        m = []
        m.extend(self._write_metadata())

        for map in self.maps:
            m.extend(map.write_string())
        return m

    def write_file(self, file_path: str):
        """ Writes the file to file_path specified """
        with open(file_path, "w+", encoding="utf8") as f:
            f.writelines(self.write())

    def _read_maps(self, maps: List[str], bpms: SMBpmList,
                   stops: List[SMStop]):
        self.maps = [
            SMMap.read_string(note_str=map, bpms=bpms, stops=stops)
            for map in maps
        ]

    def rate(self, by: float) -> SMMapSet:
        """ Changes the rate of the map """
        sms = super(SMMapSet, self).rate(by=by)
        sms.sample_start /= by
        sms.sample_length /= by

        return sms

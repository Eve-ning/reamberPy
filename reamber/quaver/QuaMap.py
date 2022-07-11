from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict

import yaml
from yaml import CLoader, CDumper, CSafeLoader

from reamber.base.Map import Map
from reamber.base.Property import map_props, stack_props
from reamber.base.lists.TimedList import TimedList
from reamber.quaver.QuaBpm import QuaBpm
from reamber.quaver.QuaMapMeta import QuaMapMeta
from reamber.quaver.QuaSv import QuaSv
from reamber.quaver.lists.QuaBpmList import QuaBpmList
from reamber.quaver.lists.QuaSvList import QuaSvList
from reamber.quaver.lists.notes.QuaHitList import QuaHitList
from reamber.quaver.lists.notes.QuaHoldList import QuaHoldList
from reamber.quaver.lists.notes.QuaNoteList import QuaNoteList


@map_props()
@dataclass
class QuaMap(Map[QuaNoteList, QuaHitList, QuaHoldList, QuaBpmList],
             QuaMapMeta):
    _props = dict(svs=QuaSvList)
    objs: Dict[str, TimedList] = \
        field(init=False,
              default_factory=lambda: dict(svs=QuaSvList([]),
                                           hits=QuaHitList([]),
                                           holds=QuaHoldList([]),
                                           bpms=QuaBpmList([])))

    @staticmethod
    def read(lines: List[str] | str, safe: bool = True) -> QuaMap:
        """Reads a .qua, loads inplace, hence it doesn't return anything

        Notes:
            Safe loading is slower, using yaml.CSafeLoader, otherwise CLoader

        Args:
            lines: The lines of .qua file.
            safe: Whether the source is trusted, unsafe loading is faster
        """

        m = QuaMap()

        file = yaml.safe_load(
            lines if isinstance(lines, str) else "\n".join(lines) + "\n",
            # Loader=CSafeLoader if safe else CLoader
        )

        # We pop them so as to reduce the size needed to pass to _readMeta
        m._read_notes(file.pop('HitObjects'))
        m._read_bpms(file.pop('TimingPoints'))
        m._read_svs(file.pop('SliderVelocities'))
        m._read_metadata(file)

        return m

    @staticmethod
    def read_file(file_path: str | Path) -> QuaMap:
        """Reads a .qua file"""

        with open(Path(file_path), "r", encoding="utf-8") as f:
            file = f.read().split("\n")

        return QuaMap.read(file)

    def write(self) -> str:
        """Writes a .qua, returns the .qua string"""
        file = self._write_meta()

        file['TimingPoints'] = self.bpms.to_yaml()
        file['SliderVelocities'] = self.svs.to_yaml()
        file['HitObjects'] = [*self.hits.to_yaml(),
                              *self.holds.to_yaml()]

        return yaml.dump(file,
                         default_flow_style=False, sort_keys=False,
                         Dumper=CDumper, allow_unicode=True)

    def write_file(self, file_path: str | Path):
        """Writes a .qua file"""

        with open(Path(file_path), "w+", encoding="utf8") as f:
            f.write(self.write())

    def _read_bpms(self, bpms: List[Dict]):
        self.bpms = QuaBpmList(
            [QuaBpm(offset=b.get('StartTime', 0),
                    bpm=b.get('Bpm', 120)) for b in bpms]
        )

    def _read_svs(self, svs: List[Dict]):
        self.svs = QuaSvList(
            [QuaSv(offset=sv.get('StartTime', 0),
                   multiplier=sv.get('Multiplier', 1.0)) for sv in svs]
        )

    def _read_notes(self, notes: List[Dict]):
        hits, holds = [], []
        for n in notes:
            if "EndTime" not in n.keys():
                hits.append(n)
            else:
                holds.append(n)
        self.hits = QuaHitList.from_yaml(hits)
        self.holds = QuaHoldList.from_yaml(holds)

    # noinspection PyMethodOverriding
    def metadata(self) -> str:
        """Grabs the map metadata"""

        return f"{self.artist} - {self.title}, {self.difficulty_name} " \
               f"({self.creator})"

    @stack_props()
    class Stacker(Map.Stacker):
        _props = ["keysounds"]

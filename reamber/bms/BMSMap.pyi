from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, TypeVar, Type

import pandas as pd

from reamber.algorithms.timing import TimingMap
from reamber.base.Map import Map
from reamber.base.lists.TimedList import TimedList
from reamber.bms.BMSChannel import BMSChannel
from reamber.bms.BMSMapMeta import BMSMapMeta
from reamber.bms.lists import BMSBpmList
from reamber.bms.lists.notes import BMSNoteList, BMSHitList, BMSHoldList

T = TypeVar('T', bound=TimedList)


@dataclass
class BMSMap(Map[BMSNoteList, BMSHitList, BMSHoldList, BMSBpmList],
             BMSMapMeta):
    _tm: TimingMap = field(init=False)
    objs: Dict[str, TimedList] = field(init=False, default_factory=lambda: ...)

    @staticmethod
    def read(lines: List[str],
             note_channel_config: dict = BMSChannel.BME) -> BMSMap: ...

    @staticmethod
    def read_file(file_path: str,
                  note_channel_config: dict = BMSChannel.BME) -> BMSMap: ...

    def write(self, note_channel_config: dict = BMSChannel.BME,
              no_sample_default: bytes = b'01') -> bytes: ...

    def write_file(self, file_path: str,
                   note_channel_config: dict = BMSChannel.BME,
                   no_sample_default: bytes = b'01'): ...

    def _read_file_header(self, data: dict): ...

    def _write_file_header(self) -> bytes: ...

    def _read_notes(self, data: List[dict], config: dict): ...

    def _reparse_bpm(self): ...

    def _write_notes(self,
                     note_channel_config: dict,
                     no_sample_default: bytes = b'01'): ...

    def metadata(self, unicode=True, **kwargs) -> str: ...

    class Stacker(Map.Stacker):
        @property
        def sample(self) -> pd.Series: ...

        @sample.setter
        def sample(self, val) -> None: ...

    def stack(self, include_types: Tuple[Type[T]] = None) -> Stacker: ...

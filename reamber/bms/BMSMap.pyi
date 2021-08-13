from __future__ import annotations

import codecs
import logging
from collections import namedtuple
from dataclasses import dataclass, field
from typing import List, Dict

import numpy as np
import pandas as pd

from reamber.base.Map import Map
from reamber.base.lists.TimedList import TimedList
from reamber.bms.BMSChannel import BMSChannel
from reamber.bms.BMSMapMeta import BMSMapMeta
from reamber.algorithms.timing import TimingMap
from reamber.bms.lists import BMSBpmList
from reamber.bms.lists.notes import BMSNoteList, BMSHitList, BMSHoldList

log = logging.getLogger(__name__)
ENCODING = "shift_jis"

DEFAULT_BEAT_PER_MEASURE = 4
MAX_KEYS = 18


@dataclass
class BMSMap(Map[BMSNoteList, BMSHitList, BMSHoldList, BMSBpmList], BMSMapMeta):

    _tm: TimingMap = field(init=False)
    objs: Dict[str, TimedList] = field(init=False, default_factory=lambda: ...)

    @staticmethod
    def read(lines: List[str], note_channel_config: dict = BMSChannel.BME) -> BMSMap: ...
    @staticmethod
    def read_file(file_path: str, note_channel_config: dict = BMSChannel.BME) -> BMSMap: ...
    def write(self, note_channel_config: dict = BMSChannel.BME, no_sample_default: bytes = b'01') -> bytes: ...
    def write_file(self, file_path: str, note_channel_config: dict = BMSChannel.BME,
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

    def stack(self, include:List[str] = None) -> Stacker: ...

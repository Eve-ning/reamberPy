from __future__ import annotations

from typing import List, Union, TYPE_CHECKING

from reamber.base.Timed import Timed
if TYPE_CHECKING:
    from reamber.base.lists.BpmList import BpmList


class Bpm(Timed):

    _props = dict(bpm='float',
                  metronome='float')

    def __init__(self, offset: float, bpm: float, metronome: float = 4, **kwargs): ...

    @property
    def beat_length(self) -> float: ...
    @property
    def metronome_length(self) -> float: ...
    @property
    def bpm(self) -> float: ...
    @bpm.setter
    def bpm(self, val) -> None: ...
    @property
    def metronome(self) -> float: ...
    @metronome.setter
    def metronome(self, val) -> None: ...
    def beat(self, bpms: List[Bpm]): ...
    @staticmethod
    def snap_exact(offsets: List[float], bpms: List[Bpm], snap_precision: int = 64): ...
    @staticmethod
    def get_beats(offsets: Union[List[float], List[Timed], float],
                  bpms: 'BpmList') -> List[float]: ...
    @staticmethod
    def align_bpms(bpms: 'BpmList',
                   BEAT_ERROR_THRESHOLD: float = 0.001,
                   BEAT_CORRECTION_FACTOR: float = 5.0) -> List[Bpm]: ...


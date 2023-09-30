from __future__ import annotations

from reamber.base.Timed import Timed


class Bpm(Timed):

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

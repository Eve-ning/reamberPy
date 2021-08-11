from __future__ import annotations

from reamber.base.Note import Note


class HoldTail(Note):

    def __init__(self, offset: float, column: int, length: float, **kwargs): ...
    @property
    def length(self) -> float: ...
    @length.setter
    def length(self, val) -> None: ...


class Hold(Note):

    def __init__(self, offset: float, column: int, length: float, **kwargs): ...
    @property
    def length(self) -> float: ...
    @length.setter
    def length(self, val) -> None: ...
    @property
    def tail_offset(self) -> float: ...


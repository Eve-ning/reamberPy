from __future__ import annotations

from reamber.base.Note import Note


class HoldTail(Note):

    _props = dict(length='float')
    def __init__(self, offset: float, column: int, length: float, **kwargs): ...
    @property
    def length(self) -> float: ...
    @length.setter
    def length(self, val) -> None: ...


class Hold(Note):

    _props = dict(length='float')
    def __init__(self, offset: float, column: int, length: float, **kwargs): ...
    @property
    def length(self) -> float: ...
    @length.setter
    def length(self, val) -> None: ...
    @property
    def tail_offset(self) -> float: ...


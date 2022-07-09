from reamber.base.Timed import Timed


class SMStop(Timed):
    def __init__(self, offset: float, length: float, **kwargs): ...

    @property
    def length(self) -> float: ...

    @length.setter
    def length(self, val) -> None: ...

from reamber.base.Timed import Timed


class Note(Timed):
    _props = dict(column=['int', 0])

    def __init__(self, offset: float, column: int, **kwargs): ...
    @property
    def column(self) -> int: ...
    @column.setter
    def column(self, val) -> None: ...
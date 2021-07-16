import pandas as pd


class OsuNoteMeta:
    @staticmethod
    def x_axis_to_column(x_axis: float, keys: int, clip: bool = True) -> int: ...
    @staticmethod
    def column_to_x_axis(column: float, keys: int) -> int: ...
    @staticmethod
    def is_hit(s: str) -> bool: ...
    @staticmethod
    def is_hold(s: str) -> bool: ...
    @property
    def hitsound_set(self) -> int: ...
    @hitsound_set.setter
    def hitsound_set(self, val) -> None: ...
    @property
    def sample_set(self) -> int: ...
    @sample_set.setter
    def sample_set(self, val) -> None: ...
    @property
    def addition_set(self) -> int: ...
    @addition_set.setter
    def addition_set(self, val) -> None: ...
    @property
    def custom_set(self) -> int: ...
    @custom_set.setter
    def custom_set(self, val) -> None: ...
    @property
    def volume(self) -> int: ...
    @volume.setter
    def volume(self, val) -> None: ...
    @property
    def hitsound_file(self) -> str: ...
    @hitsound_file.setter
    def hitsound_file(self, val) -> None: ...
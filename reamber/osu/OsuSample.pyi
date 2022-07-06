from __future__ import annotations

from typing import Dict, overload

from reamber.base.Timed import Timed


class OsuSample(Timed):
    def __init__(self, offset: float, sample_file: str = '', volume: int = 70,
                 **kwargs): ...

    @staticmethod
    @overload
    def read_string(s: str, as_dict: bool = False) -> OsuSample: ...

    @staticmethod
    @overload
    def read_string(s: str, as_dict: bool = True) -> Dict[str]: ...

    @staticmethod
    def read_string(s: str, as_dict: bool = True) -> OsuSample or Dict[
        str]: ...

    def write_string(self) -> str: ...

    @property
    def sample_file(self) -> str: ...

    @sample_file.setter
    def sample_file(self, val) -> None: ...

    @property
    def volume(self) -> str: ...

    @volume.setter
    def volume(self, val) -> None: ...

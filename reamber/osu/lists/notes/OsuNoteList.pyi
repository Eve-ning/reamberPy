from __future__ import annotations

from abc import ABC
from typing import TypeVar

import pandas as pd

from reamber.base.lists.notes.NoteList import NoteList

Item = TypeVar('Item')


class OsuNoteList(NoteList[Item], ABC):
    @property
    def hitsound_set(self) -> pd.Series: ...

    @hitsound_set.setter
    def hitsound_set(self, val) -> None: ...

    @property
    def sample_set(self) -> pd.Series: ...

    @sample_set.setter
    def sample_set(self, val) -> None: ...

    @property
    def addition_set(self) -> pd.Series: ...

    @addition_set.setter
    def addition_set(self, val) -> None: ...

    @property
    def custom_set(self) -> pd.Series: ...

    @custom_set.setter
    def custom_set(self, val) -> None: ...

    @property
    def volume(self) -> pd.Series: ...

    @volume.setter
    def volume(self, val) -> None: ...

    @property
    def hitsound_file(self) -> pd.Series: ...

    @hitsound_file.setter
    def hitsound_file(self, val) -> None: ...

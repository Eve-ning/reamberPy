from __future__ import annotations

from abc import ABC
from typing import TypeVar

import pandas as pd

from reamber.base.lists.notes.NoteList import NoteList

Item = TypeVar('Item')

class QuaNoteList(NoteList[Item], ABC):
    @property
    def hitsound_set(self) -> pd.Series: ...
    @hitsound_set.setter
    def hitsound_set(self, val) -> None: ...

from abc import ABC
from typing import TypeVar

import pandas as pd

from reamber.base.lists.notes.NoteList import NoteList

Item = TypeVar('Item')


class BMSNoteList(NoteList[Item], ABC):
    @property
    def sample(self) -> pd.Series: ...

    @sample.setter
    def sample(self, val) -> None: ...

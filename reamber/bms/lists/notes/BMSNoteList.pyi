from abc import ABC
from typing import List, Type, TypeVar

import pandas as pd

from reamber.base.Property import list_props
from reamber.base.lists.notes.NoteList import NoteList
from reamber.bms.BMSHit import BMSHit

Item = TypeVar('Item')

class BMSNoteList(NoteList[Item], ABC):
    @property
    def sample(self) -> pd.Series: ...
    @sample.setter
    def sample(self, val) -> None: ...

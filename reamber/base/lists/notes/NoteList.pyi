from __future__ import annotations

import pandas as pd

from reamber.base.Note import Note
from reamber.base.lists.TimedList import TimedList


class NoteList(TimedList[Note]):
    @property
    def column(self) -> pd.Series: ...

    @column.setter
    def column(self, val) -> None: ...

    @property
    def offset(self) -> pd.Series: ...

    @offset.setter
    def offset(self, val) -> None: ...

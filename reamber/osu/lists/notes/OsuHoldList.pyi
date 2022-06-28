from __future__ import annotations

from typing import List

from reamber.base.lists.notes.HoldList import HoldList
from reamber.osu.OsuHold import OsuHold
from reamber.osu.lists.notes.OsuNoteList import OsuNoteList


class OsuHoldList(HoldList[OsuHold], OsuNoteList[OsuHold]):
    @staticmethod
    def read(strings: List[str], keys: int) -> OsuHoldList: ...

    def write(self, keys: int) -> List[str]: ...

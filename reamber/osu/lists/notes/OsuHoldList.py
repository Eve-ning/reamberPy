from __future__ import annotations

from typing import List

import pandas as pd

from reamber.base.Property import list_props
from reamber.base.lists.notes.HoldList import HoldList
from reamber.osu.OsuHold import OsuHold
from reamber.osu.lists.notes.OsuNoteList import OsuNoteList


@list_props(OsuHold)
class OsuHoldList(HoldList[OsuHold], OsuNoteList[OsuHold]):

    @staticmethod
    def read(strings: List[str], keys: int) -> OsuHoldList:
        return OsuHoldList(pd.DataFrame(
            [OsuHold.read_string(s, keys, as_dict=True) for s in
             strings]) if strings else [])

    def write(self, keys: int) -> List[str]:
        return [h.write_string(keys) for h in self]

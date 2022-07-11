from __future__ import annotations

from typing import List

import pandas as pd

from reamber.base.Property import list_props
from reamber.base.lists.notes.HitList import HitList
from reamber.osu.OsuHit import OsuHit
from reamber.osu.lists.notes.OsuNoteList import OsuNoteList


@list_props(OsuHit)
class OsuHitList(HitList[OsuHit], OsuNoteList[OsuHit]):

    @staticmethod
    def read(strings: List[str], keys: int) -> OsuHitList:
        return OsuHitList(pd.DataFrame(
            [OsuHit.read_string(s, keys, True) for s in
             strings]) if strings else [])

    def write(self, keys: int) -> List[str]:
        return [h.write_string(keys) for h in self]

    @staticmethod
    def read_editor_string(s: str) -> OsuHitList:
        """Reads an editor string, must be of the correct format.

        Notes:
            i.e. XX:XX:XXX(OFFSET|COL, OFFSET|COL, ...) -
        """
        return OsuHitList(
            [OsuHit(offset=float(note.split("|")[0]),
                    column=int(note.split("|")[1]))
             for note in s[s.find("(") + 1: s.find(")")].split(",")]
        )

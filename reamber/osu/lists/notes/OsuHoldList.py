from __future__ import annotations

from typing import List, Union, overload, Any, Generator

import pandas as pd

from reamber.base.lists.notes.HoldList import HoldList
from reamber.osu.OsuHold import OsuHold
from reamber.osu.lists.notes.OsuNoteList import OsuNoteList


class OsuHoldList(OsuNoteList[OsuHold], HoldList[OsuHold]):

    @staticmethod
    def _init_empty() -> dict:
        """ Initializes the DataFrame if no objects are passed to init. """
        return dict(**OsuNoteList._init_empty(), **HoldList._init_empty())

    @staticmethod
    def read(strings: List[str], keys: int) -> OsuHoldList:
        """ A shortcut to reading OsuHit in a loop to create a OsuHoldList

        :param strings: A List of strings to loop through OsuHold.read
        :param keys: The number of keys
        """
        return OsuHoldList([OsuHold.read_string(s, keys) for s in strings])

    def write(self, keys: int) -> List[str]:
        return [h.write_string(keys) for h in self]


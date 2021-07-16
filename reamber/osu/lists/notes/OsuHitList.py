from __future__ import annotations

from typing import List, Union, overload, Any, Generator

import pandas as pd

from reamber.osu.OsuHit import OsuHit
from reamber.osu.lists.notes.OsuNoteList import OsuNoteList


class OsuHitList(OsuNoteList[OsuHit]):

    @staticmethod
    def _init_empty() -> dict:
        """ Initializes the DataFrame if no objects are passed to init. """
        return dict(**OsuNoteList._init_empty())

    @staticmethod
    def read(strings: List[str], keys: int) -> OsuHitList:
        """ A shortcut to reading OsuHit in a loop to create a OsuHitList

        :param strings: A List of strings to loop through OsuHit.read
        :param keys: The number of keys
        """
        return OsuHitList([OsuHit.read_string(s, keys) for s in strings])

    def write(self, keys: int) -> List[str]:
        return [h.write_string(keys) for h in self]

    @staticmethod
    def read_editor_string(s: str) -> OsuHitList:
        """ Reads an editor string, must be of the correct format.

        i.e. XX:XX:XXX(OFFSET|COL, OFFSET|COL, ...) -

        :param s: The editor string
        :return: Returns this class initialized
        """
        return OsuHitList([OsuHit(offset=float(note.split("|")[0]),
                                     column=int(note.split("|")[1]))
                           for note in s[s.find("(") + 1: s.find(")")].split(",")])


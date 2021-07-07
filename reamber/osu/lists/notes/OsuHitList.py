from __future__ import annotations

from typing import List

from reamber.osu.OsuHit import OsuHit
from reamber.osu.lists.notes.OsuNoteList import OsuNoteList


class OsuHitList(List[OsuHit], OsuNoteList):

    def _upcast(self, obj_list: List = None) -> OsuHitList:
        """ This is to facilitate inherited functions to work

        :param obj_list: The List to cast
        :rtype: OsuHitList
        """
        return OsuHitList(obj_list)

    def data(self) -> List[OsuHit]:
        return self

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

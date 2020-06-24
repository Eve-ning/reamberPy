from __future__ import annotations
from reamber.osu.lists.notes.OsuNoteList import OsuNoteList
from reamber.osu.OsuHitObj import OsuHitObj
from typing import List


class OsuHitList(List[OsuHitObj], OsuNoteList):

    def _upcast(self, objList: List = None) -> OsuHitList:
        """ This is to facilitate inherited functions to work

        :param objList: The List to cast
        :rtype: OsuHitList
        """
        return OsuHitList(objList)

    def data(self) -> List[OsuHitObj]:
        return self

    @staticmethod
    def readEditorString(s: str) -> OsuHitList:
        """ Reads an editor string, must be of the correct format.

        i.e. XX:XX:XXX(OFFSET|COL, OFFSET|COL, ...) -

        :param s: The editor string
        :return: Returns this class initialized
        """
        return OsuHitList([OsuHitObj(offset=float(note.split("|")[0]),
                                     column=int(note.split("|")[1]))
                           for note in s[s.find("(") + 1: s.find(")")].split(",")])

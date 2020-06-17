from __future__ import annotations
from reamber.base.lists.NotePkg import NotePkg
from reamber.osu.lists.notes.OsuHitList import OsuHitList
from reamber.osu.lists.notes.OsuHoldList import OsuHoldList
from reamber.osu.lists.notes.OsuNoteList import OsuNoteList
from typing import Dict, overload


class OsuNotePkg(NotePkg):
    """ This package holds both the hits and holds for each OsuMapObj """

    @overload
    def __init__(self): ...
    @overload
    def __init__(self, dataDict: Dict[str, OsuNoteList]): ...
    @overload
    def __init__(self, hits: OsuHitList, holds: OsuHoldList): ...
    def __init__(self, dataDict=None, hits=None, holds=None):
        """ Initialize a package,

        Can initialize with either overloaded method.

        :param dataDict: The data dictionary, it'll be directly assigned to dataDict. The names must explicitly match
        :param hits: The hits as a OsuHitList
        :param holds: The holds as a OsuHoldList
        """
        if dataDict is not None: self.dataDict = dataDict
        elif hits is not None:   self.dataDict = {'hits': hits, 'holds': holds}
        else: self.dataDict: Dict[str, OsuNoteList] = {'hits': OsuHitList(), 'holds': OsuHoldList()}

    def _upcast(self, dataDict: Dict[str, OsuNoteList]) -> OsuNotePkg:
        """ This is to facilitate inherited functions to work """
        return OsuNotePkg(dataDict)

    def __iter__(self):
        """ Yields the Dictionary item by item """
        yield from self.dataDict

    def data(self) -> Dict[str, OsuNoteList]:
        """ Returns the data dictionary of lists """
        return self.dataDict

    # noinspection PyTypeChecker
    def hits(self) -> OsuHitList:
        """ Returns the hitList from the dictionary """
        return self.dataDict['hits']
    # noinspection PyTypeChecker
    def holds(self) -> OsuHoldList:
        """ Returns the holdList from the dictionary """
        return self.dataDict['holds']

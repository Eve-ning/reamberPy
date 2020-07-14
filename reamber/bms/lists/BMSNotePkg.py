from __future__ import annotations

from typing import Dict, overload

from reamber.base.lists.NotePkg import NotePkg
from reamber.bms.lists.notes.BMSHitList import BMSHitList
from reamber.bms.lists.notes.BMSHoldList import BMSHoldList
from reamber.bms.lists.notes.BMSNoteList import BMSNoteList


class BMSNotePkg(NotePkg):
    """ This package holds both the hits and holds for each BMSMap """

    @overload
    def __init__(self): ...
    @overload
    def __init__(self, dataDict: Dict[str, BMSNoteList]): ...
    @overload
    def __init__(self, hits: BMSHitList, holds: BMSHoldList): ...
    def __init__(self, dataDict=None, hits=None, holds=None):
        """ Initialize a package,

        Can initialize with either overloaded method.

        :param dataDict: The data dictionary, it'll be directly assigned to dataDict. The names must explicitly match
        :param hits: The hits as a BMSHitList
        :param holds: The holds as a BMSHoldList
        """
        if dataDict is not None: self.dataDict = dataDict
        elif hits is not None:   self.dataDict = {'hits': hits, 'holds': holds}
        else: self.dataDict: Dict[str, BMSNoteList] = {'hits': BMSHitList(), 'holds': BMSHoldList()}

    def _upcast(self, dataDict: Dict[str, BMSNoteList]) -> BMSNotePkg:
        """ This is to facilitate inherited functions to work """
        return BMSNotePkg(dataDict)

    def __iter__(self):
        """ Yields the Dictionary item by item """
        yield from self.dataDict

    def data(self) -> Dict[str, BMSNoteList]:
        """ Returns the data dictionary of lists """
        return self.dataDict

    # noinspection PyTypeChecker
    def hits(self) -> BMSHitList:
        """ Returns the hitList from the dictionary """
        return self.dataDict['hits']
    # noinspection PyTypeChecker
    def holds(self) -> BMSHoldList:
        """ Returns the holdList from the dictionary """
        return self.dataDict['holds']

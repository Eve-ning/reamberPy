from __future__ import annotations

from typing import Dict, overload

from reamber.base.lists.NotePkg import NotePkg
from reamber.dummy.lists.notes.DmHitList import DmHitList
from reamber.dummy.lists.notes.DmHoldList import DmHoldList
from reamber.dummy.lists.notes.DmNoteList import DmNoteList


class DmNotePkg(NotePkg):
    """ This package holds both the hits and holds for each DmMap """

    @overload
    def __init__(self): ...
    @overload
    def __init__(self, dataDict: Dict[str, DmNoteList]): ...
    @overload
    def __init__(self, hits: DmHitList, holds: DmHoldList): ...
    def __init__(self, dataDict=None, hits=None, holds=None):
        """ Initialize a package,

        Can initialize with either overloaded method.

        :param dataDict: The data dictionary, it'll be directly assigned to dataDict. The names must explicitly match
        :param hits: The hits as a DmHitList
        :param holds: The holds as a DmHoldList
        """
        if dataDict is not None: self.dataDict = dataDict
        elif hits is not None:   self.dataDict = {'hits': hits, 'holds': holds}
        else: self.dataDict: Dict[str, DmNoteList] = {'hits': DmHitList(), 'holds': DmHoldList()}

    def _upcast(self, dataDict: Dict[str, DmNoteList]) -> DmNotePkg:
        """ This is to facilitate inherited functions to work """
        return DmNotePkg(dataDict)

    def __iter__(self):
        """ Yields the Dictionary item by item """
        yield from self.dataDict

    def data(self) -> Dict[str, DmNoteList]:
        """ Returns the data dictionary of lists """
        return self.dataDict

    # noinspection PyTypeChecker
    def hits(self) -> DmHitList:
        """ Returns the hitList from the dictionary """
        return self.dataDict['hits']
    # noinspection PyTypeChecker
    def holds(self) -> DmHoldList:
        """ Returns the holdList from the dictionary """
        return self.dataDict['holds']

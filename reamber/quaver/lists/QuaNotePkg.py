from __future__ import annotations
from reamber.base.lists.NotePkg import NotePkg
from reamber.quaver.lists.notes.QuaHitList import QuaHitList
from reamber.quaver.lists.notes.QuaHoldList import QuaHoldList
from reamber.quaver.lists.notes.QuaNoteList import QuaNoteList
from typing import Dict, overload


class QuaNotePkg(NotePkg):
    """ This package holds both the hits and holds for each QuaMapObj """

    @overload
    def __init__(self): ...
    @overload
    def __init__(self, dataDict: Dict[str, QuaNoteList]): ...
    @overload
    def __init__(self, hits: QuaHitList, holds: QuaHoldList): ...
    def __init__(self, dataDict=None, hits=None, holds=None):
        """ Initialize a package,

        Can initialize with either overloaded method.

        :param dataDict: The data dictionary, it'll be directly assigned to dataDict. The names must explicitly match
        :param hits: The hits as a QuaHitList
        :param holds: The holds as a QuaHoldList
        """
        if dataDict is not None: self.dataDict = dataDict
        elif hits is not None: self.dataDict = {'hits': hits, 'holds': holds}
        else: self.dataDict: Dict[str, QuaNoteList] = {'hits': QuaHitList(), 'holds': QuaHoldList()}

    def _upcast(self, dataDict: Dict[str, QuaNoteList]) -> QuaNotePkg:
        """ This is to facilitate inherited functions to work """
        return QuaNotePkg(dataDict)

    def __iter__(self):
        """ Yields the Dictionary item by item """
        yield from self.dataDict

    def data(self) -> Dict[str, QuaNoteList]:
        """ Returns the data dictionary of lists """
        return self.dataDict

    # noinspection PyTypeChecker
    def hits(self) -> QuaHitList:
        """ Returns the hitList from the dictionary """
        return self.dataDict['hits']
    # noinspection PyTypeChecker
    def holds(self) -> QuaHoldList:
        """ Returns the holdList from the dictionary """
        return self.dataDict['holds']

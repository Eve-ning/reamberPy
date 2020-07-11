from __future__ import annotations

from typing import Dict, overload

from reamber.base.lists.NotePkg import NotePkg
from reamber.o2jam.lists.notes.O2JHitList import O2JHitList
from reamber.o2jam.lists.notes.O2JHoldList import O2JHoldList
from reamber.o2jam.lists.notes.O2JNoteList import O2JNoteList


class O2JNotePkg(NotePkg):
    """ This package holds both the hits and holds for each O2JMap """

    @overload
    def __init__(self): ...
    @overload
    def __init__(self, dataDict: Dict[str, O2JNoteList]): ...
    @overload
    def __init__(self, hits: O2JHitList, holds: O2JHoldList): ...
    def __init__(self, dataDict=None, hits=None, holds=None):
        """ Initialize a package,

        Can initialize with either overloaded method.

        :param dataDict: The data dictionary, it'll be directly assigned to dataDict. The names must explicitly match
        :param hits: The hits as a O2JHitList
        :param holds: The holds as a O2JHoldList
        """
        if dataDict is not None: self.dataDict = dataDict
        elif hits is not None:   self.dataDict = {'hits': hits, 'holds': holds}
        else: self.dataDict: Dict[str, O2JNoteList] = {'hits': O2JHitList(), 'holds': O2JHoldList()}

    def _upcast(self, dataDict: Dict[str, O2JNoteList]) -> O2JNotePkg:
        """ This is to facilitate inherited functions to work """
        return O2JNotePkg(dataDict)

    def __iter__(self):
        """ Yields the Dictionary item by item """
        yield from self.dataDict

    def data(self) -> Dict[str, O2JNoteList]:
        """ Returns the data dictionary of lists """
        return self.dataDict

    # noinspection PyTypeChecker
    def hits(self) -> O2JHitList:
        """ Returns the hitList from the dictionary """
        return self.dataDict['hits']
    # noinspection PyTypeChecker
    def holds(self) -> O2JHoldList:
        """ Returns the holdList from the dictionary """
        return self.dataDict['holds']

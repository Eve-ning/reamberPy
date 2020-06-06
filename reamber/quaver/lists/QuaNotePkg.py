from __future__ import annotations
from reamber.base.lists.NotePkg import NotePkg
from reamber.quaver.lists.notes.QuaHitList import QuaHitList
from reamber.quaver.lists.notes.QuaHoldList import QuaHoldList
from reamber.quaver.lists.notes.QuaNoteList import QuaNoteList
from typing import Dict, overload


class QuaNotePkg(NotePkg):

    dataDict: Dict[str, QuaNoteList] = {'hits': QuaHitList(),
                                        'holds': QuaHoldList()}

    @overload
    def __init__(self): ...
    @overload
    def __init__(self, dataDict: Dict[str, QuaNoteList]): ...
    @overload
    def __init__(self, hits: QuaHitList, holds: QuaHoldList): ...
    def __init__(self, dataDict=None, hits=None, holds=None):
        if dataDict is not None: self.dataDict = dataDict
        elif hits is not None: self.dataDict = {'hits': hits, 'holds': holds}

    def _upcast(self, dataDict: Dict[str, QuaNoteList]) -> QuaNotePkg:
        return QuaNotePkg(dataDict)

    def __iter__(self):
        yield from self.dataDict

    def data(self) -> Dict[str, QuaNoteList]:
        return self.dataDict

    # noinspection PyTypeChecker
    def hits(self) -> QuaHitList:   return self.dataDict['hits']
    # noinspection PyTypeChecker
    def holds(self) -> QuaHoldList: return self.dataDict['holds']

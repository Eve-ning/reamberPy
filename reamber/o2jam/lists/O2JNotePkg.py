from __future__ import annotations
from reamber.base.lists.NotePkg import NotePkg
from reamber.o2jam.lists.notes.O2JHitList import O2JHitList
from reamber.o2jam.lists.notes.O2JHoldList import O2JHoldList
from reamber.o2jam.lists.notes.O2JNoteList import O2JNoteList
from typing import Dict, overload


class O2JNotePkg(NotePkg):

    @overload
    def __init__(self): ...
    @overload
    def __init__(self, dataDict: Dict[str, O2JNoteList]): ...
    @overload
    def __init__(self, hits: O2JHitList, holds: O2JHoldList): ...
    def __init__(self, dataDict=None, hits=None, holds=None):
        if dataDict is not None: self.dataDict = dataDict
        elif hits is not None:   self.dataDict = {'hits': hits, 'holds': holds}
        else: self.dataDict: Dict[str, O2JNoteList] = {'hits': O2JHitList(), 'holds': O2JHoldList()}

    def _upcast(self, dataDict: Dict[str, O2JNoteList]) -> O2JNotePkg:
        return O2JNotePkg(dataDict)

    def __iter__(self):
        yield from self.dataDict

    def data(self) -> Dict[str, O2JNoteList]:
        return self.dataDict

    # noinspection PyTypeChecker
    def hits(self) -> O2JHitList: return self.dataDict['hits']
    # noinspection PyTypeChecker
    def holds(self) -> O2JHoldList: return self.dataDict['holds']

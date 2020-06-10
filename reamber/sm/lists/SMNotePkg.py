from __future__ import annotations
from reamber.base.lists.NotePkg import NotePkg
from reamber.sm.lists.notes import *
from typing import Dict, overload


class SMNotePkg(NotePkg):

    @overload
    def __init__(self): ...
    @overload
    def __init__(self, dataDict: Dict[str, SMNoteList]): ...
    @overload
    def __init__(self, hits: SMHitList, holds: SMHoldList, rolls: SMRollList, mines: SMMineList,
                 lifts: SMLiftList, fakes: SMFakeList, keySounds: SMKeySoundList): ...
    def __init__(self, dataDict=None, hits=None, holds=None, rolls=None, mines=None, lifts=None, fakes=None,
                 keySounds=None):
        if dataDict is not None: self.dataDict = dataDict
        elif hits is not None: self.dataDict = {'hits': hits, 'holds': holds, 'rolls': rolls, 'mines': mines,
                                                'lifts': lifts, 'fakes': fakes, 'keySounds': keySounds}
        else: self.dataDict: Dict[str, SMNoteList] = {'hits': SMHitList(), 'holds': SMHoldList(), 'rolls': SMRollList(),
                                                      'mines': SMMineList(), 'lifts': SMLiftList(),
                                                      'fakes': SMFakeList(), 'keySounds': SMKeySoundList()}

    def _upcast(self, dataDict: Dict[str, SMNoteList]) -> SMNotePkg:
        return SMNotePkg(dataDict=dataDict)

    def __iter__(self):
        yield from self.dataDict

    def data(self) -> Dict[str, SMNoteList]:
        return self.dataDict

    # noinspection PyTypeChecker
    def hits(self) -> SMHitList:           return self.dataDict['hits']
    # noinspection PyTypeChecker
    def holds(self) -> SMHoldList:         return self.dataDict['holds']
    # noinspection PyTypeChecker
    def rolls(self) -> SMRollList:         return self.dataDict['rolls']
    # noinspection PyTypeChecker
    def mines(self) -> SMMineList:         return self.dataDict['mines']
    # noinspection PyTypeChecker
    def lifts(self) -> SMLiftList:         return self.dataDict['lifts']
    # noinspection PyTypeChecker
    def fakes(self) -> SMFakeList:         return self.dataDict['fakes']
    # noinspection PyTypeChecker
    def keySounds(self) -> SMKeySoundList: return self.dataDict['keySounds']




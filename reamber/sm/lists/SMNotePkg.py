from __future__ import annotations
from reamber.base.lists.NotePkg import NotePkg
from reamber.sm.lists.notes import *
from typing import Dict, overload


class SMNotePkg(NotePkg):
    """ This package holds hits, holds, rolls, mines, lifts, fakes, keySounds for each SMMapObj """

    @overload
    def __init__(self): ...
    @overload
    def __init__(self, dataDict: Dict[str, SMNoteList]): ...
    @overload
    def __init__(self, hits: SMHitList, holds: SMHoldList, rolls: SMRollList, mines: SMMineList,
                 lifts: SMLiftList, fakes: SMFakeList, keySounds: SMKeySoundList): ...
    def __init__(self, dataDict=None, hits=None, holds=None, rolls=None, mines=None, lifts=None, fakes=None,
                 keySounds=None):
        """ Initialize a package,

        Can initialize with either overloaded method.

        :param dataDict: The data dictionary, it'll be directly assigned to dataDict. The names must explicitly match
        :param hits: The hits as a SMHitList
        :param holds: The holds as a SMHoldList
        :param rolls: The holds as a SMRollList
        :param mines: The holds as a SMMineList
        :param lifts: The holds as a SMLiftList
        :param fakes: The holds as a SMFakeList
        :param keySounds: The holds as a SMKeySoundList
        """
        if dataDict is not None: self.dataDict = dataDict
        elif hits is not None: self.dataDict = {'hits': hits, 'holds': holds, 'rolls': rolls, 'mines': mines,
                                                'lifts': lifts, 'fakes': fakes, 'keySounds': keySounds}
        else: self.dataDict: Dict[str, SMNoteList] = {'hits': SMHitList(), 'holds': SMHoldList(), 'rolls': SMRollList(),
                                                      'mines': SMMineList(), 'lifts': SMLiftList(),
                                                      'fakes': SMFakeList(), 'keySounds': SMKeySoundList()}

    def _upcast(self, dataDict: Dict[str, SMNoteList]) -> SMNotePkg:
        """ This is to facilitate inherited functions to work """
        return SMNotePkg(dataDict=dataDict)

    def __iter__(self):
        """ Yields the Dictionary item by item """
        yield from self.dataDict

    def data(self) -> Dict[str, SMNoteList]:
        """ Returns the data dictionary of lists """
        return self.dataDict

    # noinspection PyTypeChecker
    def hits(self) -> SMHitList:
        """ Returns the hitList from the dictionary """
        return self.dataDict['hits']
    # noinspection PyTypeChecker
    def holds(self) -> SMHoldList:
        """ Returns the holdList from the dictionary """
        return self.dataDict['holds']
    # noinspection PyTypeChecker
    def rolls(self) -> SMRollList:
        """ Returns the rollList from the dictionary """
        return self.dataDict['rolls']
    # noinspection PyTypeChecker
    def mines(self) -> SMMineList:
        """ Returns the mineList from the dictionary """
        return self.dataDict['mines']
    # noinspection PyTypeChecker
    def lifts(self) -> SMLiftList:
        """ Returns the liftList from the dictionary """
        return self.dataDict['lifts']
    # noinspection PyTypeChecker
    def fakes(self) -> SMFakeList:
        """ Returns the fakeList from the dictionary """
        return self.dataDict['fakes']
    # noinspection PyTypeChecker
    def keySounds(self) -> SMKeySoundList:
        """ Returns the keySoundList from the dictionary """
        return self.dataDict['keySounds']




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
    def __init__(self, data_dict: Dict[str, BMSNoteList]): ...
    @overload
    def __init__(self, hits: BMSHitList, holds: BMSHoldList): ...
    def __init__(self, data_dict=None, hits=None, holds=None):
        """ Initialize a package,

        Can initialize with either overloaded method.

        :param data_dict: The data dictionary, it'll be directly assigned to data_dict. The names must explicitly match
        :param hits: The hits as a BMSHitList
        :param holds: The holds as a BMSHoldList
        """
        if data_dict is not None: self.data_dict = data_dict
        elif hits is not None:   self.data_dict = {'hits': hits, 'holds': holds}
        else: self.data_dict: Dict[str, BMSNoteList] = {'hits': BMSHitList(), 'holds': BMSHoldList()}

    def _upcast(self, data_dict: Dict[str, BMSNoteList]) -> BMSNotePkg:
        """ This is to facilitate inherited functions to work """
        return BMSNotePkg(data_dict)

    def __iter__(self):
        """ Yields the Dictionary item by item """
        yield from self.data_dict

    def data(self) -> Dict[str, BMSNoteList]:
        """ Returns the data dictionary of lists """
        return self.data_dict

    # noinspection PyTypeChecker
    def hits(self) -> BMSHitList:
        """ Returns the hitList from the dictionary """
        return self.data_dict['hits']
    # noinspection PyTypeChecker
    def holds(self) -> BMSHoldList:
        """ Returns the holdList from the dictionary """
        return self.data_dict['holds']

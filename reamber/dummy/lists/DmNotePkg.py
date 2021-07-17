from __future__ import annotations
        
from typing import Dict, overload

from reamber.dummy.lists.notes.DmHitList import DmHitList
from reamber.dummy.lists.notes.DmHoldList import DmHoldList
from reamber.dummy.lists.notes.DmNoteList import DmNoteList


class DmNotePkg():
    """ This package holds both the hits and holds for each DmMap """

    @overload
    def __init__(self): ...
    @overload
    def __init__(self, data_dict: Dict[str, DmNoteList]): ...
    @overload
    def __init__(self, hits: DmHitList, holds: DmHoldList): ...
    def __init__(self, data_dict=None, hits=None, holds=None):
        """ Initialize a package,

        Can initialize with either overloaded method.

        :param data_dict: The data dictionary, it'll be directly assigned to data_dict. The names must explicitly match
        :param hits: The hits as a DmHitList
        :param holds: The holds as a DmHoldList
        """
        if data_dict is not None: self.data_dict = data_dict
        elif hits is not None:   self.data_dict = {'hits': hits, 'holds': holds}
        else: self.data_dict: Dict[str, DmNoteList] = {'hits': DmHitList(), 'holds': DmHoldList()}

    def _upcast(self, data_dict: Dict[str, DmNoteList]) -> DmNotePkg:
        """ This is to facilitate inherited functions to work """
        return DmNotePkg(data_dict)

    def __iter__(self):
        """ Yields the Dictionary item by item """
        yield from self.data_dict

    def data(self) -> Dict[str, DmNoteList]:
        """ Returns the data dictionary of lists """
        return self.data_dict

    # noinspection PyTypeChecker
    def hits(self) -> DmHitList:
        """ Returns the hitList from the dictionary """
        return self.data_dict['hits']
    # noinspection PyTypeChecker
    def holds(self) -> DmHoldList:
        """ Returns the holdList from the dictionary """
        return self.data_dict['holds']

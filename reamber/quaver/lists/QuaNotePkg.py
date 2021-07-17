from __future__ import annotations

from typing import Dict, overload

from reamber.quaver.lists.notes.QuaHitList import QuaHitList
from reamber.quaver.lists.notes.QuaHoldList import QuaHoldList
from reamber.quaver.lists.notes.QuaNoteList import QuaNoteList


class QuaNotePkg():
    """ This package holds both the hits and holds for each QuaMap """

    @overload
    def __init__(self): ...
    @overload
    def __init__(self, data_dict: Dict[str, QuaNoteList]): ...
    @overload
    def __init__(self, hits: QuaHitList, holds: QuaHoldList): ...
    def __init__(self, data_dict=None, hits=None, holds=None):
        """ Initialize a package,

        Can initialize with either overloaded method.

        :param data_dict: The data dictionary, it'll be directly assigned to data_dict. The names must explicitly match
        :param hits: The hits as a QuaHitList
        :param holds: The holds as a QuaHoldList
        """
        if data_dict is not None: self.data_dict = data_dict
        elif hits is not None: self.data_dict = {'hits': hits, 'holds': holds}
        else: self.data_dict: Dict[str, QuaNoteList] = {'hits': QuaHitList(), 'holds': QuaHoldList()}

    def _upcast(self, data_dict: Dict[str, QuaNoteList]) -> QuaNotePkg:
        """ This is to facilitate inherited functions to work """
        return QuaNotePkg(data_dict)

    def __iter__(self):
        """ Yields the Dictionary item by item """
        yield from self.data_dict

    def data(self) -> Dict[str, QuaNoteList]:
        """ Returns the data dictionary of lists """
        return self.data_dict

    # noinspection PyTypeChecker
    def hits(self) -> QuaHitList:
        """ Returns the hitList from the dictionary """
        return self.data_dict['hits']
    # noinspection PyTypeChecker
    def holds(self) -> QuaHoldList:
        """ Returns the holdList from the dictionary """
        return self.data_dict['holds']

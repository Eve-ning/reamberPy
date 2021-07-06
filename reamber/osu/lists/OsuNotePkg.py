from __future__ import annotations

from typing import Dict, overload

from reamber.base.lists.NotePkg import NotePkg
from reamber.osu.lists.notes.OsuHitList import OsuHitList
from reamber.osu.lists.notes.OsuHoldList import OsuHoldList
from reamber.osu.lists.notes.OsuNoteList import OsuNoteList


class OsuNotePkg(NotePkg):
    """ This package holds both the hits and holds for each OsuMap """

    @overload
    def __init__(self): ...
    @overload
    def __init__(self, data_dict: Dict[str, OsuNoteList]): ...
    @overload
    def __init__(self, hits: OsuHitList, holds: OsuHoldList): ...
    def __init__(self, data_dict=None, hits=None, holds=None):
        """ Initialize a package,

        Can initialize with either overloaded method.

        :param data_dict: The data dictionary, it'll be directly assigned to data_dict. The names must explicitly match
        :param hits: The hits as a OsuHitList
        :param holds: The holds as a OsuHoldList
        """
        if data_dict is not None: self.data_dict = data_dict
        elif hits is not None:   self.data_dict = {'hits': hits, 'holds': holds}
        else: self.data_dict: Dict[str, OsuNoteList] = {'hits': OsuHitList(), 'holds': OsuHoldList()}

    def _upcast(self, data_dict: Dict[str, OsuNoteList]) -> OsuNotePkg:
        """ This is to facilitate inherited functions to work """
        return OsuNotePkg(data_dict)

    def __iter__(self):
        """ Yields the Dictionary item by item """
        yield from self.data_dict

    def data(self) -> Dict[str, OsuNoteList]:
        """ Returns the data dictionary of lists """
        return self.data_dict

    # noinspection PyTypeChecker
    def hits(self) -> OsuHitList:
        """ Returns the hitList from the dictionary """
        return self.data_dict['hits']
    # noinspection PyTypeChecker
    def holds(self) -> OsuHoldList:
        """ Returns the holdList from the dictionary """
        return self.data_dict['holds']

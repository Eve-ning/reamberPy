from __future__ import annotations
from reamber.base.lists.NotePkg import NotePkg
from reamber.osu.lists.notes.OsuHitList import OsuHitList
from reamber.osu.lists.notes.OsuHoldList import OsuHoldList
from reamber.osu.lists.notes.OsuNoteList import OsuNoteList
from typing import Dict, overload
from dataclasses import dataclass


class OsuNotePkg(NotePkg):

    @overload
    def __init__(self): ...
    @overload
    def __init__(self, dataDict: Dict[str, OsuNoteList]): ...
    @overload
    def __init__(self, hits: OsuHitList, holds: OsuHoldList): ...
    def __init__(self, dataDict=None, hits=None, holds=None):
        if dataDict is not None: self.dataDict = dataDict
        elif hits is not None:   self.dataDict = {'hits': hits, 'holds': holds}
        else: self.dataDict: Dict[str, OsuNoteList] = {'hits': OsuHitList(), 'holds': OsuHoldList()}

    def _upcast(self, dataDict: Dict[str, OsuNoteList]) -> OsuNotePkg:
        return OsuNotePkg(dataDict)

    def __iter__(self):
        yield from self.dataDict

    def data(self) -> Dict[str, OsuNoteList]:
        return self.dataDict

    # noinspection PyTypeChecker
    def hits(self) -> OsuHitList: return self.dataDict['hits']
    # noinspection PyTypeChecker
    def holds(self) -> OsuHoldList: return self.dataDict['holds']

from __future__ import annotations

from reamber.base.lists.NotePkg import NotePkg
from reamber.osu.lists.notes.OsuHitList import OsuHitList
from reamber.osu.lists.notes.OsuHoldList import OsuHoldList
from reamber.osu.lists.notes.OsuNoteList import OsuNoteList


class OsuNotePkg(NotePkg[OsuNoteList, OsuHitList, OsuHoldList]):
    """ This package holds both the hits and holds for each OsuMap """
    pass
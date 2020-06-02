from dataclasses import dataclass
from dataclasses import field
from typing import Union, List

from reamber.base.BpmPoint import BpmPoint
from reamber.base.NoteObject import NoteObject

# noinspection PyProtectedMember
from reamber.base.mapobj.MapObjectBpms import MapObjectBpms
# noinspection PyProtectedMember
from reamber.base.mapobj.MapObjectNotes import MapObjectNotes


@dataclass
class MapObject:
    # The TRUE nature of notes and bpms is MapObjectNotes and MapObjectBpms respectively
    # The reason for having a Union with List[NoteObject] is to facilitate the __init__ generated.
    # Having a custom __init__ would break a lot of subclasses so I just used a __post_init__ correction.
    notes: Union[MapObjectNotes, List[NoteObject]] = field(default_factory=lambda: MapObjectNotes())
    bpms: Union[MapObjectBpms, List[BpmPoint]] = field(default_factory=lambda: MapObjectBpms())

    def _recast(self):
        self.notes = MapObjectNotes(self.notes)
        self.bpms = MapObjectBpms(self.bpms)

    def __post_init__(self) -> None:
        """ This corrects all List objects that can be implicitly casted as the classes """
        self._recast()

    def addOffset(self, by: float):
        """ Move all by a specific ms """
        self.notes.addOffset(by)
        self.bpms.addOffset(by)

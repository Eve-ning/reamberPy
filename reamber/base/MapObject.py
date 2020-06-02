from typing import List
from typing import Tuple
from dataclasses import dataclass
from dataclasses import field

from reamber.base.NoteObject import NoteObject
from reamber.base.HitObject import HitObject
from reamber.base.HoldObject import HoldObject
from reamber.base.BpmPoint import BpmPoint

# noinspection PyProtectedMember
from reamber.base._mapobj.MapObjectBpm import MapObjectBpm
# noinspection PyProtectedMember
from reamber.base._mapobj.MapObjectNote import MapObjectNote


@dataclass
class MapObject(MapObjectBpm, MapObjectNote):
    notes: MapObjectNote

    def addOffset(self, by: float):
        """ Move all by a specific ms """
        self.addNoteOffsets(by)
        self.addBpmOffsets(by)

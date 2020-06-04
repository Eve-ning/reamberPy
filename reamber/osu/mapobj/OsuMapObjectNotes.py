from reamber.base.mapobj.MapObjectNotes import MapObjectNotes
from reamber.osu.mapobj.notes.OsuMapObjectHits import OsuMapObjectHits
from reamber.osu.mapobj.notes.OsuMapObjectHolds import OsuMapObjectHolds
from dataclasses import dataclass, field


@dataclass
class OsuMapObjectNotes(MapObjectNotes):
    hits: OsuMapObjectHits = field(default_factory=lambda: OsuMapObjectHits())
    holds: OsuMapObjectHolds = field(default_factory=lambda: OsuMapObjectHolds())


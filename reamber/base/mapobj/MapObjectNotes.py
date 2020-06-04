from __future__ import annotations
from reamber.base.mapobj.notes.MapObjectNoteBase import MapObjectNoteBase


class MapObjectNotes:

    hits: MapObjectNoteBase
    holds: MapObjectNoteBase

    def columns(self):
        return self.hits.columns() + self.holds.columns()

    def offsets(self):
        return self.hits.columns() + self.holds.columns()

    def data(self):
        return self.hits.data() + self.holds.data()


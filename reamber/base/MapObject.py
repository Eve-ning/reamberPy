from typing import List
from typing import Tuple
from dataclasses import dataclass
from dataclasses import field

from reamber.base.NoteObject import NoteObject
from reamber.base.HitObject import HitObject
from reamber.base.HoldObject import HoldObject
from reamber.base.BpmPoint import BpmPoint


@dataclass
class MapObject:
    noteObjects: List[NoteObject] = field(default_factory=lambda: [])
    bpmPoints: List[BpmPoint] = field(default_factory=lambda: [])

    def noteObjectsSorted(self) -> List[NoteObject]:
        return sorted(self.noteObjects, key=lambda ho: ho.offset)

    def bpmPointsSorted(self) -> List[BpmPoint]:
        return sorted(self.bpmPoints, key=lambda tp: tp.offset)

    def hitObjects(self, sort: bool = False) -> List[HitObject]:
        if sort:
            return sorted([note for note in self.noteObjects if isinstance(note, HitObject)], key=lambda x: x.offset)
        else:
            return [note for note in self.noteObjects if isinstance(note, HitObject)]

    def holdObjects(self, sort: bool = False) -> List[HoldObject]:
        if sort:
            return sorted([note for note in self.noteObjects if isinstance(note, HoldObject)], key=lambda x: x.offset)
        else:
            return [note for note in self.noteObjects if isinstance(note, HoldObject)]

    def hitObjectOffsets(self, sort: bool = True) -> List[float]:
        return [ho.offset for ho in self.hitObjects(sort)]

    def holdObjectOffsets(self, sort: bool = True) -> List[Tuple[float, float]]:
        return [(ho.offset, ho.tailOffset()) for ho in self.holdObjects(sort)]

    def addNoteOffsets(self, by: float):
        for note in self.noteObjects: note.offset += by

    def addBpmOffsets(self, by: float):
        for bpm in self.bpmPoints: bpm.offset += by

    def addOffset(self, by: float):
        self.addNoteOffsets(by)
        self.addBpmOffsets(by)

    def lastNoteOffset(self) -> float:
        hos = self.noteObjectsSorted()
        lastHit = self.hitObjects()[-1]
        lastHold = self.holdObjects()[-1]

        if lastHit.offset > lastHold.offset + lastHold.length:
            return lastHit.offset
        else:
            return lastHold.offset + lastHold.length

    def firstNoteOffset(self) -> float:
        hos = self.noteObjectsSorted()
        return hos[0].offset

from typing import List
from typing import Tuple
from dataclasses import dataclass
from dataclasses import field

from src.base.NoteObject import NoteObject
from src.base.HitObject import HitObject
from src.base.HoldObject import HoldObject
from src.base.BpmPoint import BpmPoint


@dataclass
class MapObject:
    noteObjects: List[NoteObject] = field(default_factory=lambda: [])
    bpmPoints: List[BpmPoint] = field(default_factory=lambda: [])

    def noteObjectsSorted(self) -> List[NoteObject]:
        return sorted(self.noteObjects, key=lambda ho: ho.offset)

    def hitObjects(self) -> List[HitObject]:
        return [note for note in self.noteObjects if isinstance(note, HitObject)]

    def holdObjects(self) -> List[HoldObject]:
        return [note for note in self.noteObjects if isinstance(note, HoldObject)]

    def hitObjectOffsets(self) -> List[float]:
        return [ho.offset for ho in self.hitObjects()]

    def holdObjectOffsets(self) -> List[Tuple[float, float]]:
        return [(ho.offset, ho.tailOffset()) for ho in self.holdObjects()]

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

    def bpmPointsSorted(self) -> List[BpmPoint]:
        return sorted(self.bpmPoints, key=lambda tp: tp.offset)
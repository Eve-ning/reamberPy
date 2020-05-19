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
        """ Returns a copy of Sorted NoteObjs """
        return sorted(self.noteObjects, key=lambda ho: ho.offset)

    def bpmPointsSorted(self) -> List[BpmPoint]:
        """ Returns a copy of Sorted BPMs """
        return sorted(self.bpmPoints, key=lambda tp: tp.offset)

    def hitObjects(self, sort: bool = False) -> List[HitObject]:
        """ Returns a copy of (Sorted) HitObjs """
        if sort:
            return sorted([note for note in self.noteObjects if isinstance(note, HitObject)], key=lambda x: x.offset)
        else:
            return [note for note in self.noteObjects if isinstance(note, HitObject)]

    def holdObjects(self, sort: bool = False) -> List[HoldObject]:
        """ Returns a copy of (Sorted) HoldObjs """
        if sort:
            return sorted([note for note in self.noteObjects if isinstance(note, HoldObject)], key=lambda x: x.offset)
        else:
            return [note for note in self.noteObjects if isinstance(note, HoldObject)]

    def hitObjectOffsets(self, sort: bool = True) -> List[float]:
        """ Returns a copy of the HitObj Offsets """
        return [ho.offset for ho in self.hitObjects(sort)]

    def holdObjectOffsets(self, sort: bool = True) -> List[Tuple[float, float]]:
        """ Returns a copy of the HoldObj Offsets [(Head0, Tail0), (Head1, Tail1), ...]"""
        return [(ho.offset, ho.tailOffset()) for ho in self.holdObjects(sort)]

    def addNoteOffsets(self, by: float):
        """ Move all notes by a specific ms """
        for note in self.noteObjects: note.offset += by

    def addBpmOffsets(self, by: float):
        """ Move all bpms by a specific ms """
        for bpm in self.bpmPoints: bpm.offset += by

    def addOffset(self, by: float):
        """ Move all by a specific ms """
        self.addNoteOffsets(by)
        self.addBpmOffsets(by)

    def lastNoteOffset(self) -> float:
        """ Get Final Note Offset """
        hos = self.noteObjectsSorted()
        lastHit = self.hitObjects()[-1]
        lastHold = self.holdObjects()[-1]

        if lastHit.offset > lastHold.offset + lastHold.length:
            return lastHit.offset
        else:
            return lastHold.offset + lastHold.length

    def firstNoteOffset(self) -> float:
        """ Get First Note Offset """
        hos = self.noteObjectsSorted()
        return hos[0].offset

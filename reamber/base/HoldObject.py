from reamber.base.NoteObject import NoteObject
from dataclasses import dataclass


@dataclass
class HoldObject(NoteObject):
    length: float = 0.0

    def tailOffset(self) -> float:
        return self.offset + self.length

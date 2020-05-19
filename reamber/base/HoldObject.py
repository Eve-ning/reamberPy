from reamber.base.NoteObject import NoteObject
from dataclasses import dataclass


@dataclass
class HoldObject(NoteObject):
    length: float = 0.0

    def tailOffset(self) -> float:
        """ Gets the offset for the tail """
        return self.offset + self.length

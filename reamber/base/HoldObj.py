from reamber.base.NoteObj import NoteObj
from dataclasses import dataclass


@dataclass
class HoldObj(NoteObj):
    length: float = 0.0

    def tailOffset(self) -> float:
        """ Gets the offset for the tail """
        return self.offset + self.length

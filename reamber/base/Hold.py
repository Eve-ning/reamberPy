from reamber.base.Note import Note
from dataclasses import dataclass


@dataclass
class Hold(Note):
    """ A holdable timed object with a specified length.

    We only store the length, the tail offset is calculated. """
    length: float = 0.0

    def tailOffset(self) -> float:
        """ Gets the offset for the tail """
        return self.offset + self.length

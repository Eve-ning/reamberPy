from reamber.base.Note import Note
from dataclasses import dataclass


@dataclass
class PtnNote(Note):
    """ Just a subclass to separate the interfaces. """
    confidence: float = 1.0

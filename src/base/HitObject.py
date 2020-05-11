from src.base.NoteObject import NoteObject
from dataclasses import dataclass


@dataclass
class HitObject(NoteObject):
    # This is an empty class to separate HITS and HOLDS
    pass

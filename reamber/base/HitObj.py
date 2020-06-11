from reamber.base.NoteObj import NoteObj
from dataclasses import dataclass


@dataclass
class HitObj(NoteObj):
    # This is an empty class to separate HITS and HOLDS
    pass

from dataclasses import dataclass
from reamber.base.TimedObj import TimedObj


@dataclass
class NoteObj(TimedObj):
    column: int = 0

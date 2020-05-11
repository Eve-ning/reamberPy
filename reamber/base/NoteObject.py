from dataclasses import dataclass
from reamber.base.TimedObject import TimedObject


@dataclass
class NoteObject(TimedObject):
    column: int = 0

from dataclasses import dataclass
from src.base.TimedObject import TimedObject


@dataclass
class NoteObject(TimedObject):
    column: int = 0

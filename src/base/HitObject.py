from src.base.TimedObject import TimedObject as TimedObject
from dataclasses import dataclass


@dataclass
class HitObject(TimedObject):
    column: int = 0

from src.base.MapObject import MapObject
from src.sm.SMMapObjectMeta import SMMapObjectMeta
from dataclasses import dataclass

@dataclass
class SMMapObject(MapObject, SMMapObjectMeta):
    pass

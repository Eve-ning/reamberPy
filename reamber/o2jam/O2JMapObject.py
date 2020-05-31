from dataclasses import dataclass
from reamber.base.MapObject import MapObject
from reamber.o2jam.O2JMapObjectMeta import O2JMapObjectMeta
from reamber.o2jam.O2JEventPackage import O2JEventPackage

import struct


@dataclass
class O2JMapObject(MapObject, O2JMapObjectMeta):
    def readFile(self, filePath: str):
        with open(filePath, "rb") as f:
            self.readMeta(f.read(300))
            O2JEventPackage.readEventPackages(f.read(), self.bpm)

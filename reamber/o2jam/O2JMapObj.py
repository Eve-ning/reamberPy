from dataclasses import dataclass

from reamber.base.MapObj import MapObj
from reamber.o2jam.O2JEventPackage import O2JEventPackage
from reamber.o2jam.O2JMapObjMeta import O2JMapObjMeta


@dataclass
class O2JMapObj(MapObj, O2JMapObjMeta):
    def readFile(self, filePath: str):
        with open(filePath, "rb") as f:
            self.readMeta(f.read(300))
            O2JEventPackage.readEventPackages(f.read(), self.bpm)

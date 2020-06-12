from dataclasses import dataclass, field

from reamber.o2jam.O2JEventPackage import O2JEventPackage
from reamber.o2jam.O2JMapSetObjMeta import O2JMapSetObjMeta
from reamber.o2jam.O2JMapObj import O2JMapObj
from typing import List

import logging

log = logging.getLogger(__name__)

@dataclass
class O2JMapSetObj(O2JMapSetObjMeta):
    """ We won't support OJM for now, we'll just deal with OJN since it's much easier. """

    maps: List[O2JMapObj] = field(default_factory=lambda: [])

    # noinspection PyUnresolvedReferences
    def readFile(self, filePath: str):
        with open(filePath, "rb") as f:
            self.readMeta(f.read(300))

            mapPkgs = O2JEventPackage.readEventPackages(f.read(), self.bpm, self.packageCount)
            for pkgs in mapPkgs:
                self.maps.append(O2JMapObj.readPkgs(pkgs=pkgs, initBpm=self.bpm))
            pass

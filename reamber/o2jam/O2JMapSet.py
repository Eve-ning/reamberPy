from dataclasses import dataclass, field

from reamber.o2jam.O2JEventPackage import O2JEventPackage
from reamber.o2jam.O2JMapSetMeta import O2JMapSetMeta
from reamber.o2jam.O2JMap import O2JMap
from typing import List

import logging

log = logging.getLogger(__name__)

@dataclass
class O2JMapSet(O2JMapSetMeta):
    """ This holds all data of OJN with a few exceptions

    Exceptions:
     - Cover Data
     - Key Sounds Data + Placement

    This also doesn't support OJM (IO) and OJN (O).

    OJM is not supported due to its complexity. OJN writing isn't supported due to lack of support.

    We won't support OJM for now, we'll just deal with OJN since it's much easier. """

    maps: List[O2JMap] = field(default_factory=lambda: [])

    def readFile(self, filePath: str):
        """ Reads the OJN file. Do not load the OJM file.

        :param filePath: Path to the ojn file.
        """

        self.__init__()

        with open(filePath, "rb") as f:
            self.readMeta(f.read(300))

            mapPkgs = O2JEventPackage.readEventPackages(f.read(), self.packageCount)
            for pkgs in mapPkgs:
                self.maps.append(O2JMap.readPkgs(pkgs=pkgs, initBpm=self.bpm))
            pass

    # def writeFile(self, filePath: str):
    #     with open(filePath, 'wb+') as f:
    #         self.writeMeta(f)

    def describe(self, rounding: int = 2, unicode: bool = False) -> None:
        """ Describes the map's attributes as a short summary

        :param rounding: The decimal rounding
        :param unicode: Whether to attempt to get the non-unicode or unicode. \
            Doesn't attempt to translate.
        """

        for m in self.maps:
            m.describe(rounding=rounding, unicode=unicode, s=self)
            print("="*20)

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import List

from reamber.base.MapSet import MapSet
from reamber.o2jam.O2JEventPackage import O2JEventPackage
from reamber.o2jam.O2JMap import O2JMap
from reamber.o2jam.O2JMapSetMeta import O2JMapSetMeta

log = logging.getLogger(__name__)

@dataclass
class O2JMapSet(O2JMapSetMeta, MapSet):
    """ This holds all data of OJN with a few exceptions

    Exceptions:
     - Cover Data
     - Key Sounds Data + Placement

    This also doesn't support OJM (IO) and OJN (O).

    OJM is not supported due to its complexity. OJN writing isn't supported due to lack of support.

    We won't support OJM for now, we'll just deal with OJN since it's much easier. """

    maps: List[O2JMap] = field(default_factory=lambda: [])

    @staticmethod
    def read(b: bytes) -> O2JMapSet:
        """ Reads the OJN file bytes. Do not load the OJM file.

        :param b: File Bytes
        """

        self = O2JMapSet()
        self.read_meta(b[:300])

        mapPkgs = O2JEventPackage.read_event_packages(b[300:], self.package_count)
        for pkgs in mapPkgs:
            self.maps.append(O2JMap.read_pkgs(pkgs=pkgs, init_bpm=self.bpm))

        return self

    @staticmethod
    def readFile(file_path: str) -> O2JMapSet:
        """ Reads the OJN file. Do not load the OJM file.

        :param file_path: Path to the ojn file.
        """

        with open(file_path, "rb") as f:
            b = f.read()
        return O2JMapSet.read(b)

    # def writeFile(self, file_path: str):
    #     with open(file_path, 'wb+') as f:
    #         self.writeMeta(f)

    def rate(self, by: float, inplace:bool = False):
        """ Changes the rate of the map

        :param by: The value to rate it by. 1.1x speeds up the song by 10%. Hence 10/11 of the length.
        :param inplace: Whether to perform the operation in place. Returns a copy if False
        """
        # Nothing special to change here, just a loop on rate

        return super(O2JMapSet, self).rate(by=by, inplace=inplace)

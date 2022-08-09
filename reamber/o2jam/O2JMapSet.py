from __future__ import annotations

import logging
from dataclasses import dataclass

from reamber.base.MapSet import MapSet
from reamber.o2jam.O2JEventPackage import O2JEventPackage
from reamber.o2jam.O2JMap import O2JMap
from reamber.o2jam.O2JMapSetMeta import O2JMapSetMeta
from reamber.o2jam.lists.O2JBpmList import O2JBpmList
from reamber.o2jam.lists.notes import O2JHitList
from reamber.o2jam.lists.notes.O2JHoldList import O2JHoldList
from reamber.o2jam.lists.notes.O2JNoteList import O2JNoteList

log = logging.getLogger(__name__)


@dataclass
class O2JMapSet(MapSet[O2JNoteList, O2JHitList, O2JHoldList,
                       O2JBpmList, O2JMap], O2JMapSetMeta):
    """This holds all data of OJN with a few exceptions

    Notes:
        Exceptions:
         - Cover Data
         - Key Sounds Data + Placement

        This also doesn't support OJM (IO) and OJN (O).

        OJM is not supported due to its complexity. OJN writing isn't
        supported due to lack of support.

        We won't support OJM for now, we'll just deal with OJN since
        it's much easier.
    """

    def level_name(self, o2j: O2JMap) -> int:
        return self.level[[id(i) for i in self].index(id(o2j))]

    @staticmethod
    def read(b: bytes) -> O2JMapSet:
        """Reads the OJN file bytes. Do not load the OJM file.

        Args
            b: File Bytes
        """

        ms = O2JMapSet()
        ms.read_meta(b[:300])

        maps_pkg = O2JEventPackage.read_event_packages(
            b[300:], ms.package_count
        )
        for map_pkg in maps_pkg:
            ms.maps.append(O2JMap.read_pkgs(pkgs=map_pkg, init_bpm=ms.bpm))

        return ms

    @staticmethod
    def read_file(file_path: str) -> O2JMapSet:
        """Reads the OJN file. Do not load the OJM file.

        Args:
            file_path: Path to the ojn file.
        """

        with open(file_path, "rb") as f:
            b = f.read()
        return O2JMapSet.read(b)

    class Stacker(MapSet.Stacker):
        ...

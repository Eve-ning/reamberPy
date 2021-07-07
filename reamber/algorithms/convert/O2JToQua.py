from typing import List

from reamber.base.Bpm import Bpm
from reamber.o2jam.O2JMapSet import O2JMapSet, O2JMap
from reamber.quaver.QuaBpm import QuaBpm
from reamber.quaver.QuaHit import QuaHit
from reamber.quaver.QuaHold import QuaHold
from reamber.quaver.QuaMap import QuaMap
from reamber.quaver.QuaMapMeta import QuaMapMode
from reamber.quaver.lists.QuaBpmList import QuaBpmList
from reamber.quaver.lists.QuaNotePkg import QuaNotePkg
from reamber.quaver.lists.notes.QuaHitList import QuaHitList
from reamber.quaver.lists.notes.QuaHoldList import QuaHoldList


class O2JToQua:
    @staticmethod
    def convert(o2j: O2JMapSet) -> List[QuaMap]:
        """ Converts a Mapset to multiple Quaver maps

        Note that a mapset contains maps, so a list would be expected.
        O2JMap conversion is not possible due to lack of O2JMapset Metadata

        :param o2j:
        :return:
        """
        quaMapSet: List[QuaMap] = []
        for o2jMap in o2j.maps:
            assert isinstance(o2jMap, O2JMap)
            hits: List[QuaHit] = []
            holds: List[QuaHold] = []

            # Note Conversion
            for hit in o2jMap.notes.hits():
                hits.append(QuaHit(offset=hit.offset, column=hit.column))
            for hold in o2jMap.notes.holds():
                holds.append(QuaHold(offset=hold.offset, column=hold.column, _length=hold.length))

            bpms: List[Bpm] = []

            # Timing Point Conversion
            for bpm in o2jMap.bpms:
                bpms.append(QuaBpm(offset=bpm.offset, bpm=bpm.bpm))

            # Extract Metadata
            quaMap = QuaMap(
                title=o2j.title,
                artist=o2j.artist,
                creator=o2j.creator,
                mode=QuaMapMode.KEYS_7,
                difficulty_name=f"Level {o2j.level[o2j.maps.index(o2jMap)]}",
                bpms=QuaBpmList(bpms),
                notes=QuaNotePkg(hits=QuaHitList(hits),
                                 holds=QuaHoldList(holds))
            )
            quaMapSet.append(quaMap)
        return quaMapSet

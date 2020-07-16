import codecs
from typing import List

from reamber.base.Bpm import Bpm
from reamber.bms.BMSBpm import BMSBpm
from reamber.bms.BMSHit import BMSHit
from reamber.bms.BMSHold import BMSHold
from reamber.bms.BMSMap import BMSMap
from reamber.bms.lists.BMSBpmList import BMSBpmList
from reamber.bms.lists.BMSNotePkg import BMSNotePkg
from reamber.bms.lists.notes.BMSHitList import BMSHitList
from reamber.bms.lists.notes.BMSHoldList import BMSHoldList
from reamber.o2jam.O2JMapSet import O2JMapSet, O2JMap


class O2JToBMS:
    @staticmethod
    def convert(o2j: O2JMapSet) -> List[BMSMap]:
        """ Converts a Mapset to multiple BMS maps

        Note that a mapset contains maps, so a list would be expected.
        O2JMap conversion is not possible due to lack of O2JMapset Metadata

        :param o2j:
        :return:
        """

        bmsMapSet: List[BMSMap] = []
        for o2jMap in o2j.maps:
            assert isinstance(o2jMap, O2JMap)

            hits: List[BMSHit] = []
            holds: List[BMSHold] = []

            # Note Conversion
            for hit in o2jMap.notes.hits():
                hits.append(BMSHit(offset=hit.offset, column=hit.column + 1))
            for hold in o2jMap.notes.holds():
                holds.append(BMSHold(offset=hold.offset, column=hold.column + 1, _length=hold.length))

            bpms: List[Bpm] = []

            # Timing Point Conversion
            for bpm in o2jMap.bpms:
                bpms.append(BMSBpm(offset=bpm.offset, bpm=bpm.bpm))

            # Extract Metadata
            bmsMap = BMSMap(
                title=codecs.encode(o2j.title, encoding='shift_jis'),
                artist=codecs.encode(o2j.artist, encoding='shift_jis'),
                version=codecs.encode(f"{o2j.level[o2j.maps.index(o2jMap)]}", encoding='shift_jis'),
                bpms=BMSBpmList(bpms),
                notes=BMSNotePkg(hits=BMSHitList(hits),
                                 holds=BMSHoldList(holds))
            )
            bmsMapSet.append(bmsMap)
        return bmsMapSet

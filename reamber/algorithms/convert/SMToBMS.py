from typing import List

from reamber.base.Bpm import Bpm
from reamber.sm.SMMapSet import SMMapSet, SMMap
from reamber.bms.BMSBpm import BMSBpm
from reamber.bms.BMSHit import BMSHit
from reamber.bms.BMSHold import BMSHold
from reamber.bms.BMSMap import BMSMap
from reamber.bms.lists.BMSBpmList import BMSBpmList
from reamber.bms.lists.BMSNotePkg import BMSNotePkg
from reamber.bms.lists.notes.BMSHitList import BMSHitList
from reamber.bms.lists.notes.BMSHoldList import BMSHoldList


class SMToBMS:
    @staticmethod
    def convert(sm: SMMapSet) -> List[BMSMap]:
        """ Converts a Mapset to multiple BMS maps

        Not too sure how you would convert this, but I'm providing the API anyways.

        Make sure to verify the writeFile arguments so that the writing works

        :param sm:
        :return:
        """

        bmsMapSet: List[BMSMap] = []
        for smMap in sm.maps:
            assert isinstance(smMap, SMMap)

            hits: List[BMSHit] = []
            holds: List[BMSHold] = []

            # Note Conversion
            for hit in smMap.notes.hits():
                if hit.column == 0: continue
                hits.append(BMSHit(offset=hit.offset, column=hit.column - 1))
            for hold in smMap.notes.holds():
                if hold.column == 0: continue
                holds.append(BMSHold(offset=hold.offset, column=hold.column - 1, _length=hold.length))

            bpms: List[Bpm] = []

            # Timing Point Conversion
            for bpm in smMap.bpms:
                bpms.append(BMSBpm(offset=bpm.offset, bpm=bpm.bpm))

            # Extract Metadata
            bmsMap = BMSMap(
                title=sm.title,
                artist=sm.artist,
                version=f"{smMap.difficulty} {smMap.difficultyVal}",
                bpms=BMSBpmList(bpms),
                notes=BMSNotePkg(hits=BMSHitList(hits),
                                 holds=BMSHoldList(holds))
            )
            bmsMapSet.append(bmsMap)
        return bmsMapSet

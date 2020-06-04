from reamber.sm.SMMapSetObject import SMMapSetObject, SMMapObject
from reamber.quaver.QuaMapObject import QuaMapObject
from reamber.quaver.QuaHitObject import QuaHitObject
from reamber.quaver.QuaHoldObject import QuaHoldObject
from reamber.quaver.QuaBpmPoint import QuaBpmPoint
from reamber.base.BpmPoint import BpmPoint
from reamber.quaver.mapobj.QuaMapObjectNotes import QuaMapObjectNotes
from reamber.quaver.mapobj.QuaMapObjectBpms import QuaMapObjectBpms
from reamber.quaver.mapobj.notes.QuaMapObjectHolds import QuaMapObjectHolds
from reamber.quaver.mapobj.notes.QuaMapObjectHits import QuaMapObjectHits
from typing import List


class SMToQua:
    @staticmethod
    def convert(sm: SMMapSetObject) -> List[QuaMapObject]:
        """ Converts a Mapset to possibly multiple quaver maps
        Note that a mapset contains maps, so a list would be expected.
        SMMap conversion is not possible due to lack of SMMapset Metadata
        :param sm: The MapSet
        :return: Quaver Maps
        """
        quaMapSet: List[QuaMapObject] = []
        for smMap in sm.maps:
            assert isinstance(smMap, SMMapObject)
            hits: List[QuaHitObject] = []
            holds: List[QuaHoldObject] = []

            # Note Conversion
            for hit in smMap.notes.hits:
                hits.append(QuaHitObject(offset=hit.offset, column=hit.column))
            for hold in smMap.notes.holds:
                holds.append(QuaHoldObject(offset=hold.offset, column=hold.column, length=hold.length))

            bpms: List[BpmPoint] = []

            # Timing Point Conversion
            for bpm in smMap.bpms:
                bpms.append(QuaBpmPoint(offset=bpm.offset, bpm=bpm.bpm))

            # Extract Metadata
            osuMap = QuaMapObject(
                backgroundFile=sm.background,
                title=sm.title,
                artist=sm.artist,
                audioFile=sm.music,
                creator=sm.credit,
                difficultyName=f"{smMap.difficulty} {smMap.difficultyVal}",
                songPreviewTime=int(sm.sampleStart),
                bpms=QuaMapObjectBpms(bpms),
                notes=QuaMapObjectNotes(hits=QuaMapObjectHits(hits),
                                        holds=QuaMapObjectHolds(holds))
            )
            quaMapSet.append(osuMap)
        return quaMapSet

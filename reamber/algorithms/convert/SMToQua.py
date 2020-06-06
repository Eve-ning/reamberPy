from reamber.sm.SMMapSetObject import SMMapSetObject, SMMapObject
from reamber.quaver.QuaMapObject import QuaMapObject
from reamber.quaver.QuaHitObject import QuaHitObject
from reamber.quaver.QuaHoldObject import QuaHoldObject
from reamber.quaver.QuaBpmObject import QuaBpmObject
from reamber.base.BpmObject import BpmObject
from reamber.quaver.lists.QuaNotePkg import QuaNotePkg
from reamber.quaver.lists.QuaBpmList import QuaBpmList
from reamber.quaver.lists.notes.QuaHoldList import QuaHoldList
from reamber.quaver.lists.notes.QuaHitList import QuaHitList
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

            bpms: List[BpmObject] = []

            # Timing Point Conversion
            for bpm in smMap.bpms:
                bpms.append(QuaBpmObject(offset=bpm.offset, bpm=bpm.bpm))

            # Extract Metadata
            osuMap = QuaMapObject(
                backgroundFile=sm.background,
                title=sm.title,
                artist=sm.artist,
                audioFile=sm.music,
                creator=sm.credit,
                difficultyName=f"{smMap.difficulty} {smMap.difficultyVal}",
                songPreviewTime=int(sm.sampleStart),
                bpms=QuaBpmList(bpms),
                notes=QuaNotePkg(hits=QuaHitList(hits),
                                 holds=QuaHoldList(holds))
            )
            quaMapSet.append(osuMap)
        return quaMapSet

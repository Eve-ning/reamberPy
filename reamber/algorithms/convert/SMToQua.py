from reamber.sm.SMMapSetObj import SMMapSetObj, SMMapObj
from reamber.quaver.QuaMapObj import QuaMapObj
from reamber.quaver.QuaHitObj import QuaHitObj
from reamber.quaver.QuaHoldObj import QuaHoldObj
from reamber.quaver.QuaBpmObj import QuaBpmObj
from reamber.base.BpmObj import BpmObj
from reamber.quaver.lists.QuaNotePkg import QuaNotePkg
from reamber.quaver.lists.QuaBpmList import QuaBpmList
from reamber.quaver.lists.notes.QuaHoldList import QuaHoldList
from reamber.quaver.lists.notes.QuaHitList import QuaHitList
from typing import List


class SMToQua:
    @staticmethod
    def convert(sm: SMMapSetObj) -> List[QuaMapObj]:
        """ Converts a Mapset to possibly multiple quaver maps
        Note that a mapset contains maps, so a list would be expected.
        SMMap conversion is not possible due to lack of SMMapset Metadata
        :param sm: The MapSet
        :return: Quaver Maps
        """
        quaMapSet: List[QuaMapObj] = []
        for smMap in sm.maps:
            assert isinstance(smMap, SMMapObj)
            hits: List[QuaHitObj] = []
            holds: List[QuaHoldObj] = []

            # Note Conversion
            for hit in smMap.notes.hits():
                hits.append(QuaHitObj(offset=hit.offset, column=hit.column))
            for hold in smMap.notes.holds():
                holds.append(QuaHoldObj(offset=hold.offset, column=hold.column, length=hold.length))

            bpms: List[BpmObj] = []

            # Timing Point Conversion
            for bpm in smMap.bpms:
                bpms.append(QuaBpmObj(offset=bpm.offset, bpm=bpm.bpm))

            # Extract Metadata
            osuMap = QuaMapObj(
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

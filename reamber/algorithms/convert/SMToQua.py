from reamber.sm.SMMapSet import SMMapSet, SMMap
from reamber.quaver.QuaMap import QuaMap
from reamber.quaver.QuaHit import QuaHit
from reamber.quaver.QuaHold import QuaHold
from reamber.quaver.QuaBpm import QuaBpm
from reamber.base.Bpm import Bpm
from reamber.quaver.lists.QuaNotePkg import QuaNotePkg
from reamber.quaver.lists.QuaBpmList import QuaBpmList
from reamber.quaver.lists.notes.QuaHoldList import QuaHoldList
from reamber.quaver.lists.notes.QuaHitList import QuaHitList
from typing import List


class SMToQua:
    @staticmethod
    def convert(sm: SMMapSet) -> List[QuaMap]:
        """ Converts a SMMapset to possibly multiple quaver maps

        Note that a mapset contains maps, so a list would be expected.
        SMMap conversion is not possible due to lack of SMMapset Metadata

        :param sm: SM Mapset
        :return: List of Quaver Maps
        """
        quaMapSet: List[QuaMap] = []
        for smMap in sm.maps:
            assert isinstance(smMap, SMMap)
            hits: List[QuaHit] = []
            holds: List[QuaHold] = []

            # Note Conversion
            for hit in smMap.notes.hits():
                hits.append(QuaHit(offset=hit.offset, column=hit.column))
            for hold in smMap.notes.holds():
                holds.append(QuaHold(offset=hold.offset, column=hold.column, length=hold.length))

            bpms: List[Bpm] = []

            # Timing Point Conversion
            for bpm in smMap.bpms:
                bpms.append(QuaBpm(offset=bpm.offset, bpm=bpm.bpm))

            # Extract Metadata
            quaMap = QuaMap(
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
            quaMapSet.append(quaMap)
        return quaMapSet

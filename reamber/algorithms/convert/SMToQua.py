from typing import List

from reamber.base.Bpm import Bpm
from reamber.quaver.QuaBpm import QuaBpm
from reamber.quaver.QuaHit import QuaHit
from reamber.quaver.QuaHold import QuaHold
from reamber.quaver.QuaMap import QuaMap
from reamber.quaver.QuaMapMeta import QuaMapMode
from reamber.quaver.lists.QuaBpmList import QuaBpmList
from reamber.quaver.lists.QuaNotePkg import QuaNotePkg
from reamber.quaver.lists.notes.QuaHitList import QuaHitList
from reamber.quaver.lists.notes.QuaHoldList import QuaHoldList
from reamber.sm.SMMapMeta import SMMapChartTypes
from reamber.sm.SMMapSet import SMMapSet, SMMap


class SMToQua:
    @staticmethod
    def convert(sm: SMMapSet, assertKeys=True) -> List[QuaMap]:
        """ Converts a SMMapset to possibly multiple quaver maps

        Note that a mapset contains maps, so a list would be expected.
        SMMap conversion is not possible due to lack of SMMapset Metadata

        :param sm:
        :param assertKeys: Adds an assertion to verify that Quaver can support this key mode
        :return:
        """
        quaMapSet: List[QuaMap] = []
        for smMap in sm.maps:
            assert isinstance(smMap, SMMap)
            if assertKeys: assert QuaMapMode.get_mode(int(SMMapChartTypes.get_keys(smMap.chart_type))) != "",\
                f"Current Chart Type, Keys:{int(SMMapChartTypes.get_keys(smMap.chart_type))} is not supported"

            hits: List[QuaHit] = []
            holds: List[QuaHold] = []

            # Note Conversion
            for hit in smMap.notes.hits():
                hits.append(QuaHit(offset=hit.offset, column=hit.column))
            for hold in smMap.notes.holds():
                holds.append(QuaHold(offset=hold.offset, column=hold.column, _length=hold.length))

            bpms: List[Bpm] = []

            # Timing Point Conversion
            for bpm in smMap.bpms:
                bpms.append(QuaBpm(offset=bpm.offset, bpm=bpm.bpm))

            # Extract Metadata
            quaMap = QuaMap(
                backgroundFile=sm.background,
                title=sm.title,
                artist=sm.artist,
                mode=QuaMapMode.get_mode(int(SMMapChartTypes.get_keys(smMap.chart_type))),
                audioFile=sm.music,
                creator=sm.credit,
                difficultyName=f"{smMap.difficulty} {smMap.difficulty_val}",
                songPreviewTime=int(sm.sample_start),
                bpms=QuaBpmList(bpms),
                notes=QuaNotePkg(hits=QuaHitList(hits),
                                 holds=QuaHoldList(holds))
            )
            quaMapSet.append(quaMap)
        return quaMapSet

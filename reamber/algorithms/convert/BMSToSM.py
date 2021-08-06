from typing import List

from unidecode import unidecode

from reamber.base.Bpm import Bpm
from reamber.bms.BMSMap import BMSMap
from reamber.sm.SMBpm import SMBpm
from reamber.sm.SMHit import SMHit
from reamber.sm.SMHold import SMHold
from reamber.sm.SMMapMeta import SMMapChartTypes
from reamber.sm.SMMapSet import SMMapSet, SMMap
from reamber.sm.lists.SMBpmList import SMBpmList
from reamber.sm.lists.notes.SMHitList import SMHitList
from reamber.sm.lists.notes.SMHoldList import SMHoldList


class BMSToSM:
    @staticmethod
    def convert(bms: BMSMap) -> SMMapSet:
        """ Converts a Mapset to multiple SM maps

        :param bms:
        :return:
        """

        bpms: List[Bpm] = []
        for bpm in bms.bpms:
            bpms.append(SMBpm(offset=bpm.offset, bpm=bpm.bpm))

        hits: List[SMHit] = []
        holds: List[SMHold] = []

        for hit in bms.notes.hits():
            hits.append(SMHit(offset=hit.offset, column=hit.column))
        for hold in bms.notes.holds():
            holds.append(SMHold(offset=hold.offset, column=hold.column, _length=hold.length))

        smSet: SMMapSet = SMMapSet(
            title=unidecode(bms.title.decode('sjis')),
            artist=unidecode(bms.artist.decode('sjis')),
            offset=0.0,
            maps=[
                SMMap(
                    description=unidecode(bms.version.decode('sjis')),
                    chart_type=SMMapChartTypes.get_type(bms.notes.max_column() + 1),
                    notes=SMNotePkg(hits=SMHitList(hits),
                                    holds=SMHoldList(holds)),
                    bpms=SMBpmList(bpms)
                )
            ]
        )

        return smSet

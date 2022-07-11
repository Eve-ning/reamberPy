from unidecode import unidecode

from reamber.algorithms.convert.ConvertBase import ConvertBase
from reamber.bms.BMSMap import BMSMap
from reamber.sm.SMMap import SMMap
from reamber.sm.SMMapMeta import SMMapChartTypes
from reamber.sm.SMMapSet import SMMapSet
from reamber.sm.lists.SMBpmList import SMBpmList
from reamber.sm.lists.notes.SMHitList import SMHitList
from reamber.sm.lists.notes.SMHoldList import SMHoldList


class BMSToSM(ConvertBase):
    @classmethod
    def convert(cls, bms: BMSMap) -> SMMapSet:
        """Converts a Mapset to multiple SM maps"""

        sm = SMMap()
        sm.hits = cls.cast(
            bms.hits, SMHitList, dict(offset='offset', column='column')
        )
        sm.holds = cls.cast(
            bms.holds, SMHoldList,
            dict(offset='offset', column='column', length='length')
        )
        sm.bpms = cls.cast(
            bms.bpms, SMBpmList, dict(offset='offset', bpm='bpm')
        )

        sm.description = unidecode(bms.version.decode('sjis'))
        sm.chart_type = SMMapChartTypes.get_type(bms.stack().column.max() + 1)
        sms = SMMapSet()
        sms.maps = [sm]

        sms.title = unidecode(bms.title.decode('sjis'))
        sms.artist = unidecode(bms.artist.decode('sjis'))
        sms.offset = 0.0

        return sms

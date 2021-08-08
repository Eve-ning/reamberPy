import codecs
from typing import List

from reamber.algorithms.convert.ConvertBase import ConvertBase
from reamber.bms.BMSMap import BMSMap
from reamber.bms.lists.BMSBpmList import BMSBpmList
from reamber.bms.lists.notes.BMSHitList import BMSHitList
from reamber.bms.lists.notes.BMSHoldList import BMSHoldList
from reamber.sm.SMMapSet import SMMapSet


class SMToBMS(ConvertBase):
    @classmethod
    def convert(cls, sm: SMMapSet) -> List[BMSMap]:
        """ Converts a Mapset to multiple BMS maps

        Not too sure how you would convert this, but I'm providing the API anyways.
        """

        bmss: List[BMSMap] = []
        for sm in sm.maps:
            bms = BMSMap()
            bms.hits = cls.cast(sm.hits, BMSHitList, dict(offset='offset', column='column'))
            bms.holds = cls.cast(sm.holds, BMSHoldList, dict(offset='offset', column='column', length='length'))
            bms.bpms = cls.cast(sm.bpms, BMSBpmList, dict(offset='offset', bpm='bpm'))

            bms.title = codecs.encode(sm.title, encoding='shift_jis')
            bms.artist = codecs.encode(sm.artist, encoding='shift_jis')
            bms.version = codecs.encode(f"{sm.difficulty} {sm.difficulty_val}", encoding='shift_jis')

            bmss.append(bms)
        return bmss

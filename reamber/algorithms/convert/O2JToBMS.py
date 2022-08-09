import codecs
from typing import List

from reamber.algorithms.convert.ConvertBase import ConvertBase
from reamber.bms.BMSMap import BMSMap
from reamber.bms.lists.BMSBpmList import BMSBpmList
from reamber.bms.lists.notes.BMSHitList import BMSHitList
from reamber.bms.lists.notes.BMSHoldList import BMSHoldList
from reamber.o2jam.O2JMapSet import O2JMapSet


class O2JToBMS(ConvertBase):
    @classmethod
    def convert(cls, o2js: O2JMapSet, move_right_by: int = 1) -> List[BMSMap]:
        """Converts a Mapset to multiple BMS maps

        Note:
            Column 0 is the scratch.

            Thus, converting 7k with ``moveRightBy == 1`` to remove the
            first column scratch

        Args:
            o2js: O2Jam Mapset
            move_right_by: Moves every column to the right by
        """

        bmss: List[BMSMap] = []
        for o2j in o2js:
            bms = BMSMap()
            bms.hits = cls.cast(
                o2j.hits, BMSHitList, dict(offset='offset', column='column')
            )
            bms.holds = cls.cast(
                o2j.holds, BMSHoldList,
                dict(offset='offset', column='column', length='length')
            )
            bms.bpms = cls.cast(
                o2j.bpms, BMSBpmList, dict(offset='offset', bpm='bpm')
            )
            bms.stack().column += move_right_by

            bms.title = codecs.encode(o2js.title, encoding='shift_jis')
            bms.artist = codecs.encode(o2js.artist, encoding='shift_jis')
            bms.version = codecs.encode(
                f"{o2js.level_name(o2j)}", encoding='shift_jis'
            )

            bmss.append(bms)
        return bmss

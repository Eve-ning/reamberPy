import codecs

from reamber.algorithms.convert.ConvertBase import ConvertBase
from reamber.bms.BMSMap import BMSMap
from reamber.bms.lists.BMSBpmList import BMSBpmList
from reamber.bms.lists.notes.BMSHitList import BMSHitList
from reamber.bms.lists.notes.BMSHoldList import BMSHoldList
from reamber.osu.OsuMap import OsuMap


class OsuToBMS(ConvertBase):
    @classmethod
    def convert(cls, osu: OsuMap, move_right_by: int = 0) -> BMSMap:
        """Converts osu to a BMS map

        Note:
            Column 0 is the scratch.

            Thus, converting 7k with ``moveRightBy == 1`` to remove the
            first column scratch

        Args:
            osu: Osu Map
            move_right_by: Moves every column to the right by
        """

        bms = BMSMap()
        bms.hits = cls.cast(
            osu.hits, BMSHitList, dict(offset='offset', column='column')
        )
        bms.holds = cls.cast(
            osu.holds, BMSHoldList,
            dict(offset='offset', column='column', length='length')
        )
        bms.bpms = cls.cast(
            osu.bpms, BMSBpmList,
            dict(offset='offset', bpm='bpm')
        )

        bms.stack().column += move_right_by

        bms.title = codecs.encode(osu.title, encoding='shift_jis')
        bms.artist = codecs.encode(osu.artist, encoding='shift_jis')
        bms.version = codecs.encode(osu.version, encoding='shift_jis')

        return bms

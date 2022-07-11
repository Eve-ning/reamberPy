from unidecode import unidecode

from reamber.algorithms.convert.ConvertBase import ConvertBase
from reamber.bms.BMSMap import BMSMap
from reamber.osu.OsuMap import OsuMap
from reamber.osu.lists.OsuBpmList import OsuBpmList
from reamber.osu.lists.notes.OsuHitList import OsuHitList
from reamber.osu.lists.notes.OsuHoldList import OsuHoldList


class BMSToOsu(ConvertBase):
    @classmethod
    def convert(cls, bms: BMSMap) -> OsuMap:
        """Converts a BMS map to an osu map"""

        osu = OsuMap()
        osu.hits = cls.cast(
            bms.hits, OsuHitList,
            dict(
                offset='offset', column='column',
                hitsound_file=bms.hits.sample.apply(str, args={'ascii'})
            )
        )
        osu.holds = cls.cast(
            bms.holds, OsuHoldList,
            dict(
                offset='offset', column='column', length='length',
                hitsound_file=bms.holds.sample.apply(str, args={'ascii'})
            )
        )
        osu.bpms = cls.cast(
            bms.bpms, OsuBpmList,
            dict(offset='offset', bpm='bpm')
        )

        osu.title = unidecode(bms.title.decode('sjis'))
        osu.version = unidecode(bms.version.decode('sjis'))
        osu.artist = unidecode(bms.artist.decode('sjis'))
        osu.circle_size = bms.stack().column.max() + 1

        return osu

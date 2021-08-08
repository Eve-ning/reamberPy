from typing import List

from reamber.algorithms.convert.ConvertBase import ConvertBase
from reamber.o2jam.O2JMapSet import O2JMapSet
from reamber.osu.OsuMap import OsuMap
from reamber.osu.lists.OsuBpmList import OsuBpmList
from reamber.osu.lists.notes.OsuHitList import OsuHitList
from reamber.osu.lists.notes.OsuHoldList import OsuHoldList


class O2JToOsu(ConvertBase):
    @classmethod
    def convert(cls, o2js: O2JMapSet) -> List[OsuMap]:
        """ Converts a Mapset to multiple Osu maps

        Note that a mapset contains maps, so a list would be expected.
        O2JMap conversion is not possible due to lack of O2JMapset Metadata

        :param o2js:
        :return:
        """

        osus: List[OsuMap] = []
        for o2j in o2js.maps:
            osu = OsuMap()
            osu.hits = cls.cast(o2j.hits, OsuHitList, dict(offset='offset', column='column'))
            osu.holds = cls.cast(o2j.holds, OsuHoldList, dict(offset='offset', column='column', length='length'))
            osu.bpms = cls.cast(o2j.bpms, OsuBpmList, dict(offset='offset', bpm='bpm'))

            osu.title = o2js.title
            osu.artist = o2js.artist
            osu.creator = o2js.creator
            osu.version = f"Level {o2js.level[o2js.maps.index(o2j)]}"
            osu.circle_size = 7
            osus.append(osu)
        return osus

from typing import List

from reamber.algorithms.convert.ConvertBase import ConvertBase
from reamber.osu.OsuMap import OsuMap
from reamber.osu.lists.OsuBpmList import OsuBpmList
from reamber.osu.lists.notes.OsuHitList import OsuHitList
from reamber.osu.lists.notes.OsuHoldList import OsuHoldList
from reamber.sm.SMMapSet import SMMapSet


class SMToOsu(ConvertBase):
    @classmethod
    def convert(cls, sms: SMMapSet) -> List[OsuMap]:
        """Converts a SMMapset to possibly multiple osu maps"""

        # I haven't tested with non 4 keys, so it might explode :(

        osus: List[OsuMap] = []
        for sm in sms:
            osu = OsuMap()
            osu.hits = cls.cast(
                sm.hits, OsuHitList,
                dict(offset='offset', column='column')
            )
            osu.holds = cls.cast(
                sm.holds, OsuHoldList,
                dict(offset='offset', column='column', length='length')
            )
            osu.bpms = cls.cast(
                sm.bpms, OsuBpmList,
                dict(offset='offset', bpm='bpm')
            )

            osu.background_file_name = sms.background
            osu.title = sms.title
            osu.title_unicode = sms.title_translit
            osu.artist = sms.artist
            osu.artist_unicode = sms.artist_translit
            osu.audio_file_name = sms.music
            osu.creator = sms.credit
            osu.version = f"{sm.difficulty} {sm.difficulty_val}"
            osu.preview_time = int(sms.sample_start)

            osus.append(osu)
        return osus

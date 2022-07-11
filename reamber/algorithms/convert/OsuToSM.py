from reamber.algorithms.convert.ConvertBase import ConvertBase
from reamber.osu.OsuMap import OsuMap
from reamber.sm.SMMap import SMMap
from reamber.sm.SMMapMeta import SMMapChartTypes
from reamber.sm.SMMapSet import SMMapSet
from reamber.sm.lists.SMBpmList import SMBpmList
from reamber.sm.lists.notes.SMHitList import SMHitList
from reamber.sm.lists.notes.SMHoldList import SMHoldList


class OsuToSM(ConvertBase):
    @classmethod
    def convert(cls, osu: OsuMap, raise_bad_mode: bool = True) -> SMMapSet:
        """Converts Osu to a SMMapset Obj

        Args:
            osu: Osu Map
            raise_bad_mode: Raises if SM can't support this key mode
        """

        sm = SMMap()

        sm.hits = cls.cast(
            osu.hits, SMHitList,
            dict(offset='offset', column='column')
        )
        sm.holds = cls.cast(
            osu.holds, SMHoldList,
            dict(offset='offset', column='column', length='length')
        )
        sm.bpms = cls.cast(
            osu.bpms, SMBpmList,
            dict(offset='offset', bpm='bpm')
        )

        sms = SMMapSet()

        sms.maps = [sm]

        sms.music = osu.audio_file_name
        sms.title = osu.title
        sms.title_translit = osu.title_unicode
        sms.artist = osu.artist
        sms.artist_translit = osu.artist_unicode
        sms.credit = osu.creator
        sms.background = osu.background_file_name
        sms.sample_start = osu.preview_time
        sms.sample_length = 10
        sms.offset = 0.0

        sm.chart_type = SMMapChartTypes.get_type(osu.stack().column.max() + 1)

        if raise_bad_mode and not sm.chart_type:
            raise ValueError(
                f"Keys {int(sm.stack().column.max() + 1)} isn't supported"
            )

        return sms

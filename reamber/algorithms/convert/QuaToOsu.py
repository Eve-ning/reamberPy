from reamber.algorithms.convert.ConvertBase import ConvertBase
from reamber.osu.OsuMap import OsuMap
from reamber.osu.lists.OsuBpmList import OsuBpmList
from reamber.osu.lists.OsuSvList import OsuSvList
from reamber.osu.lists.notes.OsuHitList import OsuHitList
from reamber.osu.lists.notes.OsuHoldList import OsuHoldList
from reamber.quaver.QuaMap import QuaMap
from reamber.quaver.QuaMapMeta import QuaMapMode


class QuaToOsu(ConvertBase):
    @classmethod
    def convert(cls, qua: QuaMap) -> OsuMap:
        """Converts a Quaver map to an osu map"""

        osu = OsuMap()
        osu.hits = cls.cast(
            qua.hits, OsuHitList,
            dict(offset='offset', column='column')
        )
        osu.holds = cls.cast(
            qua.holds, OsuHoldList,
            dict(offset='offset', column='column', length='length')
        )
        osu.bpms = cls.cast(
            qua.bpms, OsuBpmList,
            dict(offset='offset', bpm='bpm')
        )
        osu.svs = cls.cast(
            qua.svs, OsuSvList,
            dict(offset='offset', multiplier='multiplier')
        )

        osu.background_file_name = qua.background_file
        osu.circle_size = QuaMapMode.get_keys(qua.mode)
        osu.title = qua.title
        osu.title_unicode = qua.title
        osu.artist = qua.artist
        osu.artist_unicode = qua.artist
        osu.audio_file_name = qua.audio_file
        osu.creator = qua.creator
        osu.version = qua.difficulty_name
        osu.preview_time = qua.song_preview_time
        osu.tags = qua.tags

        return osu

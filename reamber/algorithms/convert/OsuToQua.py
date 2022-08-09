from reamber.algorithms.convert.ConvertBase import ConvertBase
from reamber.osu.OsuMap import OsuMap
from reamber.quaver.QuaMap import QuaMap
from reamber.quaver.QuaMapMeta import QuaMapMode
from reamber.quaver.lists import QuaBpmList
from reamber.quaver.lists import QuaSvList
from reamber.quaver.lists.notes.QuaHitList import QuaHitList
from reamber.quaver.lists.notes.QuaHoldList import QuaHoldList


class OsuToQua(ConvertBase):
    @classmethod
    def convert(cls, osu: OsuMap, raise_bad_mode: bool = True) -> QuaMap:
        """Converts Osu to a Qua Map

        Args:
            osu: Osu Map
            raise_bad_mode: Raises if Quaver can't support this key mode
        """

        qua = QuaMap()
        qua.hits = cls.cast(
            osu.hits, QuaHitList, dict(offset='offset', column='column')
        )
        qua.holds = cls.cast(
            osu.holds, QuaHoldList,
            dict(offset='offset', column='column', length='length')
        )
        qua.bpms = cls.cast(
            osu.bpms, QuaBpmList,
            dict(offset='offset', bpm='bpm')
        )
        qua.sv = cls.cast(
            osu.svs, QuaSvList,
            dict(offset='offset', multiplier='multiplier')
        )

        qua.audio_file = osu.audio_file_name
        qua.title = osu.title
        qua.mode = QuaMapMode.get_mode(int(osu.circle_size))
        qua.artist = osu.artist
        qua.creator = osu.creator
        qua.tags = osu.tags
        qua.difficulty_name = osu.version
        qua.background_file = osu.background_file_name
        qua.song_preview_time = osu.preview_time

        if raise_bad_mode and not qua.mode:
            raise ValueError(
                f"Keys {int(osu.stack().column.max() + 1)} isn't supported"
                f"by Quaver."
            )

        return qua

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
    def convert(cls, osu: OsuMap, assert_keys=True) -> QuaMap:
        """ Converts Osu to a Qua Map

        :param osu:
        :param assert_keys: Adds an assertion to verify that Quaver can support this key mode
        :return:
        """

        qua = QuaMap()
        qua.hits = cls.cast(osu.hits, QuaHitList, dict(offset='offset', column='column'))
        qua.holds = cls.cast(osu.holds, QuaHoldList, dict(offset='offset', column='column', length='length'))
        qua.bpms = cls.cast(osu.bpms, QuaBpmList, dict(offset='offset', bpm='bpm'))
        qua.sv = cls.cast(osu.svs, QuaSvList, dict(offset='offset', multiplier='multiplier'))

        qua.audio_file = osu.audio_file_name
        qua.title = osu.title
        qua.mode = QuaMapMode.get_mode(int(osu.circle_size))
        qua.artist = osu.artist
        qua.creator = osu.creator
        qua.tags = osu.tags
        qua.difficulty_name = osu.version
        qua.background_file = osu.background_file_name
        qua.song_preview_time = osu.preview_time

        if assert_keys: assert qua.mode, f"Current Keys {int(osu.stack.column.max() + 1)} is not supported"

        return qua

from typing import List

from reamber.algorithms.convert.ConvertBase import ConvertBase
from reamber.quaver.QuaMap import QuaMap
from reamber.quaver.QuaMapMeta import QuaMapMode
from reamber.quaver.lists.QuaBpmList import QuaBpmList
from reamber.quaver.lists.notes.QuaHitList import QuaHitList
from reamber.quaver.lists.notes.QuaHoldList import QuaHoldList
from reamber.sm.SMMapMeta import SMMapChartTypes
from reamber.sm.SMMapSet import SMMapSet


class SMToQua(ConvertBase):
    @classmethod
    def convert(cls, sms: SMMapSet, assert_keys=True) -> List[QuaMap]:
        """ Converts a SMMapset to possibly multiple quaver maps

        Note that a mapset contains maps, so a list would be expected.
        SMMap conversion is not possible due to lack of SMMapset Metadata

        :param sm:
        :param assert_keys: Adds an assertion to verify that Quaver can support this key mode
        :return:
        """

        quas: List[QuaMap] = []
        for sm in sms:
            qua = QuaMap()
            qua.hits = cls.cast(sm.hits, QuaHitList, dict(offset='offset', column='column'))
            qua.holds = cls.cast(sm.holds, QuaHoldList, dict(offset='offset', column='column', length='length'))
            qua.bpms = cls.cast(sm.bpms, QuaBpmList, dict(offset='offset', bpm='bpm'))

            qua.background_file_name = sm.background
            qua.background_file = sm.background
            qua.title = sm.title
            qua.artist = sm.artist
            qua.mode = QuaMapMode.get_mode(int(SMMapChartTypes.get_keys(sm.chart_type)))
            qua.audio_file = sm.music
            qua.creator = sm.credit
            qua.difficulty_name = f"{sm.difficulty} {sm.difficulty_val}"
            qua.song_preview_time = int(sm.sample_start)
            if assert_keys: assert qua.mode, f"Current Keys {int(sm.stack.column.max() + 1)} is not supported"

            quas.append(qua)
        return quas

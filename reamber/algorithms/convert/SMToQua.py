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
    def convert(cls, sms: SMMapSet, raise_bad_mode: bool = True)\
        -> List[QuaMap]:
        """Converts a SMMapset to possibly multiple quaver maps

        Args:
            sms: Stepmania Mapset
            raise_bad_mode: Raises if Quaver can't support this key mode
        """

        quas: List[QuaMap] = []
        for sm in sms:
            qua = QuaMap()
            qua.hits = cls.cast(sm.hits, QuaHitList,
                                dict(offset='offset', column='column'))
            qua.holds = cls.cast(sm.holds, QuaHoldList,
                                 dict(offset='offset', column='column',
                                      length='length'))
            qua.bpms = cls.cast(sm.bpms, QuaBpmList,
                                dict(offset='offset', bpm='bpm'))

            qua.background_file = sms.background
            qua.title = sms.title
            qua.artist = sms.artist
            qua.mode = QuaMapMode.get_mode(
                int(SMMapChartTypes.get_keys(sm.chart_type)))
            qua.audio_file = sms.music
            qua.creator = sms.credit
            qua.difficulty_name = f"{sm.difficulty} {sm.difficulty_val}"
            qua.song_preview_time = int(sms.sample_start)
            if raise_bad_mode and not qua.mode:
                raise ValueError(
                    f"Keys {int(sm.stack().column.max() + 1)} isn't supported."
                )
            quas.append(qua)
        return quas

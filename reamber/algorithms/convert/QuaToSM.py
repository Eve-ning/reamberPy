from reamber.algorithms.convert.ConvertBase import ConvertBase
from reamber.quaver.QuaMap import QuaMap
from reamber.sm.SMMap import SMMap
from reamber.sm.SMMapMeta import SMMapChartTypes
from reamber.sm.SMMapSet import SMMapSet
from reamber.sm.lists.SMBpmList import SMBpmList
from reamber.sm.lists.notes.SMHitList import SMHitList
from reamber.sm.lists.notes.SMHoldList import SMHoldList


class QuaToSM(ConvertBase):
    @classmethod
    def convert(cls, qua: QuaMap) -> SMMapSet:
        """Converts a Quaver map to a SMMapset Obj

        Notes:
             Each Quaver map will make a separate mapset
        """

        sm = SMMap()
        sm.hits = cls.cast(
            qua.hits, SMHitList,
            dict(offset='offset', column='column')
        )
        sm.holds = cls.cast(
            qua.holds, SMHoldList,
            dict(offset='offset', column='column', length='length')
        )
        sm.bpms = cls.cast(
            qua.bpms, SMBpmList,
            dict(offset='offset', bpm='bpm')
        )
        sm.chart_type = SMMapChartTypes.get_type(qua.stack().column.max() + 1)

        sms = SMMapSet()

        sms.maps = [sm]

        sms.music = qua.audio_file

        sms.title = qua.title
        sms.title_translit = qua.title
        sms.artist = qua.artist
        sms.artist_translit = qua.artist
        sms.credit = qua.creator
        sms.background = qua.background_file
        sms.sample_start = qua.song_preview_time
        sms.sample_length = 10
        sms.offset = qua.stack().offset.min()

        return sms

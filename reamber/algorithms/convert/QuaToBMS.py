import codecs

from reamber.algorithms.convert.ConvertBase import ConvertBase
from reamber.bms.BMSMap import BMSMap
from reamber.bms.lists.BMSBpmList import BMSBpmList
from reamber.bms.lists.notes.BMSHitList import BMSHitList
from reamber.bms.lists.notes.BMSHoldList import BMSHoldList
from reamber.quaver.QuaMap import QuaMap


class QuaToBMS(ConvertBase):
    @classmethod
    def convert(cls, qua: QuaMap, move_right_by: int = 0) -> BMSMap:
        """ Converts qua to a BMS map

        Note that column 0 is the scratch. e.g. you're converting a 7k you should have ``moveRightBy == 1`` so that the
        first column is not scratch

        :param move_right_by: Moves every column to the right by
        :param qua:
        :return:
        """

        bms = BMSMap()
        bms.hits = cls.cast(qua.hits, BMSHitList, dict(offset='offset', column='column'))
        bms.holds = cls.cast(qua.holds, BMSHoldList, dict(offset='offset', column='column', length='length'))
        bms.bpms = cls.cast(qua.bpms, BMSBpmList, dict(offset='offset', bpm='bpm'))

        bms.stack().column += move_right_by

        bms.title = codecs.encode(qua.title, encoding='shift_jis')
        bms.artist = codecs.encode(qua.artist, encoding='shift_jis')
        bms.version = codecs.encode(qua.difficulty_name, encoding='shift_jis')

        return bms

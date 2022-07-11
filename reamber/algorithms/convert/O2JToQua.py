from typing import List

from reamber.algorithms.convert.ConvertBase import ConvertBase
from reamber.o2jam.O2JMapSet import O2JMapSet
from reamber.quaver.QuaMap import QuaMap
from reamber.quaver.QuaMapMeta import QuaMapMode
from reamber.quaver.lists.QuaBpmList import QuaBpmList
from reamber.quaver.lists.notes.QuaHitList import QuaHitList
from reamber.quaver.lists.notes.QuaHoldList import QuaHoldList


class O2JToQua(ConvertBase):
    @classmethod
    def convert(cls, o2js: O2JMapSet) -> List[QuaMap]:
        """Converts a Mapset to multiple Quaver maps"""

        quas: List[QuaMap] = []
        for o2j in o2js:
            qua = QuaMap()
            qua.hits = cls.cast(
                o2j.hits, QuaHitList, dict(offset='offset', column='column')
            )
            qua.holds = cls.cast(
                o2j.holds, QuaHoldList,
                dict(offset='offset', column='column', length='length')
            )
            qua.bpms = cls.cast(
                o2j.bpms, QuaBpmList, dict(offset='offset', bpm='bpm')
            )

            qua.title = o2js.title
            qua.artist = o2js.artist
            qua.creator = o2js.creator
            qua.mode = QuaMapMode.KEYS_7
            qua.difficulty_name = f"Level {o2js.level_name(o2j)}"

            quas.append(qua)

        return quas

from unidecode import unidecode

from reamber.algorithms.convert.ConvertBase import ConvertBase
from reamber.bms.BMSMap import BMSMap
from reamber.quaver.QuaMap import QuaMap
from reamber.quaver.QuaMapMeta import QuaMapMode
from reamber.quaver.lists import QuaBpmList
from reamber.quaver.lists.notes.QuaHitList import QuaHitList
from reamber.quaver.lists.notes.QuaHoldList import QuaHoldList


class BMSToQua(ConvertBase):
    @classmethod
    def convert(cls, bms: BMSMap, raise_bad_mode: bool = True) -> QuaMap:
        """Converts a BMS to a Qua Map

        Args
            bms: BMS Map
            raise_bad_mode: Raises if Quaver can't support this key mode
        """

        qua = QuaMap()
        qua.hits = cls.cast(
            bms.hits, QuaHitList, dict(offset='offset', column='column')
        )
        qua.holds = cls.cast(
            bms.holds, QuaHoldList,
            dict(offset='offset', column='column', length='length')
        )
        qua.bpms = cls.cast(
            bms.bpms, QuaBpmList,
            dict(offset='offset', bpm='bpm')
        )

        qua.title = unidecode(bms.title.decode('sjis'))
        qua.mode = QuaMapMode.get_mode(int(bms.stack().column.max() + 1))
        qua.difficulty_name = unidecode(bms.version.decode('sjis'))
        qua.artist = unidecode(bms.artist.decode('sjis'))

        if raise_bad_mode and not qua.mode:
            raise ValueError(
                f"Keys {int(bms.stack().column.max() + 1)} isn't supported"
                f"by Quaver."
            )

        return qua

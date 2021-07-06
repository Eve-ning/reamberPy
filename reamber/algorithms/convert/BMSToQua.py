from typing import List

from unidecode import unidecode

from reamber.base.Bpm import Bpm
from reamber.bms.BMSMap import BMSMap
from reamber.quaver.QuaBpm import QuaBpm
from reamber.quaver.QuaHit import QuaHit
from reamber.quaver.QuaHold import QuaHold
from reamber.quaver.QuaMap import QuaMap
from reamber.quaver.QuaMapMeta import QuaMapMode
from reamber.quaver.lists import QuaBpmList
from reamber.quaver.lists import QuaNotePkg
from reamber.quaver.lists.notes.QuaHitList import QuaHitList
from reamber.quaver.lists.notes.QuaHoldList import QuaHoldList


class BMSToQua:
    @staticmethod
    def convert(bms: BMSMap, assertKeys=True) -> QuaMap:
        """ Converts a BMS to a Qua Map

        :param bms:
        :param assertKeys: Adds an assertion to verify that Quaver can support this key mode
        :return:
        """

        if assertKeys: assert QuaMapMode.getMode(int(bms.notes.max_column() + 1)) != "",\
            f"Current Keys {bms.notes.max_column() + 1} is not supported"

        hits: List[QuaHit] = []
        holds: List[QuaHold] = []

        for hit in bms.notes.hits():
            hits.append(QuaHit(offset=hit.offset, column=hit.column))
        for hold in bms.notes.holds():
            holds.append(QuaHold(offset=hold.offset, column=hold.column, _length=hold.length))

        bpms: List[Bpm] = []

        for bpm in bms.bpms:
            bpms.append(QuaBpm(offset=bpm.offset, bpm=bpm.bpm))

        qua: QuaMap = QuaMap(
            title=unidecode(bms.title.decode('sjis')),
            mode=QuaMapMode.getMode(int(bms.notes.max_column() + 1)),
            difficultyName=unidecode(bms.version.decode('sjis')),
            artist=unidecode(bms.artist.decode('sjis')),
            notes=QuaNotePkg(hits=QuaHitList(hits),
                             holds=QuaHoldList(holds)),
            bpms=QuaBpmList(bpms)
        )

        return qua

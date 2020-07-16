import codecs
from typing import List

from reamber.base.Bpm import Bpm
from reamber.bms.BMSBpm import BMSBpm
from reamber.bms.BMSHit import BMSHit
from reamber.bms.BMSHold import BMSHold
from reamber.bms.BMSMap import BMSMap
from reamber.bms.lists.BMSBpmList import BMSBpmList
from reamber.bms.lists.BMSNotePkg import BMSNotePkg
from reamber.bms.lists.notes.BMSHitList import BMSHitList
from reamber.bms.lists.notes.BMSHoldList import BMSHoldList
from reamber.osu.OsuMap import OsuMap


class OsuToBMS:
    @staticmethod
    def convert(osu: OsuMap, moveRightBy:int = 0) -> BMSMap:
        """ Converts osu to a BMS map

        Note that column 0 is the scratch. e.g. you're converting a 7k you should have ``moveRightBy == 1`` so that the
        first column is not scratch

        :param moveRightBy: Moves every column to the right by
        :param osu:
        :return:
        """

        hits: List[BMSHit] = []
        holds: List[BMSHold] = []

        # Note Conversion
        for hit in osu.notes.hits():
            hits.append(BMSHit(offset=hit.offset, column=hit.column + moveRightBy))
        for hold in osu.notes.holds():
            holds.append(BMSHold(offset=hold.offset, column=hold.column + moveRightBy, _length=hold.length))

        bpms: List[Bpm] = []

        # Timing Point Conversion
        for bpm in osu.bpms:
            bpms.append(BMSBpm(offset=bpm.offset, bpm=bpm.bpm))

        # Extract Metadata
        bmsMap = BMSMap(
            title=codecs.encode(osu.title, encoding='shift_jis'),
            artist=codecs.encode(osu.artist, encoding='shift_jis'),
            version=codecs.encode(osu.version, encoding='shift_jis'),
            bpms=BMSBpmList(bpms),
            notes=BMSNotePkg(hits=BMSHitList(hits),
                             holds=BMSHoldList(holds))
        )

        return bmsMap

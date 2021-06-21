from typing import List

from unidecode import unidecode

from reamber.base.Bpm import Bpm
from reamber.bms.BMSMap import BMSMap
from reamber.osu.OsuBpm import OsuBpm
from reamber.osu.OsuHit import OsuHit
from reamber.osu.OsuHold import OsuHold
from reamber.osu.OsuMap import OsuMap
from reamber.osu.lists.OsuBpmList import OsuBpmList
from reamber.osu.lists.OsuNotePkg import OsuNotePkg
from reamber.osu.lists.notes.OsuHitList import OsuHitList
from reamber.osu.lists.notes.OsuHoldList import OsuHoldList


class BMSToOsu:
    @staticmethod
    def convert(bms: BMSMap) -> OsuMap:
        """ Converts a BMS map to an osu map

        :param bms:
        :return:
        """

        hits: List[OsuHit] = []
        holds: List[OsuHold] = []

        # Note Conversion
        for hit in bms.notes.hits():
            hits.append(OsuHit(offset=hit.offset, column=hit.column,
                               hitsoundFile=str(hit.sample, 'ascii')))
        for hold in bms.notes.holds():
            holds.append(OsuHold(offset=hold.offset, column=hold.column, _length=hold.length,
                                 hitsoundFile=str(hold.sample, 'ascii')))

        bpms: List[Bpm] = []
        # Timing Point Conversion
        for bpm in bms.bpms:
            bpms.append(OsuBpm(offset=bpm.offset, bpm=bpm.bpm))

        # Extract Metadata
        osuMap = OsuMap(
            title=unidecode(bms.title.decode('sjis')),
            version=unidecode(bms.version.decode('sjis')),
            artist=unidecode(bms.artist.decode('sjis')),
            circleSize=bms.notes.maxColumn() + 1,
            bpms=OsuBpmList(bpms),
            notes=OsuNotePkg(hits=OsuHitList(hits),
                             holds=OsuHoldList(holds))
        )

        return osuMap

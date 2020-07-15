from typing import List

from reamber.base.Bpm import Bpm
from reamber.osu.OsuBpm import OsuBpm
from reamber.osu.OsuHit import OsuHit
from reamber.osu.OsuHold import OsuHold
from reamber.osu.OsuMap import OsuMap
from reamber.osu.lists.OsuBpmList import OsuBpmList
from reamber.osu.lists.OsuNotePkg import OsuNotePkg
from reamber.osu.lists.notes.OsuHitList import OsuHitList
from reamber.osu.lists.notes.OsuHoldList import OsuHoldList
from reamber.bms.BMSMap import BMSMap


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
            hits.append(OsuHit(offset=hit.offset, column=hit.column, hitsoundFile=hit.sample))
        for hold in bms.notes.holds():
            holds.append(OsuHold(offset=hold.offset, column=hold.column, _length=hold.length, hitsoundFile=hold.sample))

        bpms: List[Bpm] = []
        # Timing Point Conversion
        for bpm in bms.bpms:
            bpms.append(OsuBpm(offset=bpm.offset, bpm=bpm.bpm))

        # Extract Metadata
        osuMap = OsuMap(
            title=bms.title,
            circleSize=bms.notes.maxColumn() + 1,
            artist=bms.artist,
            version=bms.version,
            bpms=OsuBpmList(bpms),
            notes=OsuNotePkg(hits=OsuHitList(hits),
                             holds=OsuHoldList(holds))
        )

        return osuMap

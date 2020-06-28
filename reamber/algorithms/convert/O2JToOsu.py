from reamber.o2jam.O2JMapSet import O2JMapSet, O2JMap
from reamber.osu.OsuMap import OsuMap
from reamber.osu.OsuHit import OsuHit
from reamber.osu.OsuHold import OsuHold
from reamber.osu.OsuBpm import OsuBpm
from reamber.base.Bpm import Bpm
from reamber.osu.lists.OsuBpmList import OsuBpmList
from reamber.osu.lists.OsuNotePkg import OsuNotePkg
from reamber.osu.lists.notes.OsuHoldList import OsuHoldList
from reamber.osu.lists.notes.OsuHitList import OsuHitList
from typing import List


class O2JToOsu:
    @staticmethod
    def convert(o2j: O2JMapSet) -> List[OsuMap]:
        """ Converts a Mapset to multiple Osu maps

        Note that a mapset contains maps, so a list would be expected.
        O2JMap conversion is not possible due to lack of O2JMapset Metadata

        :param o2j: O2Jam Mapset
        :return: List of Osu Maps
        """

        osuMapSet: List[OsuMap] = []
        for o2jMap in o2j.maps:
            assert isinstance(o2jMap, O2JMap)

            hits: List[OsuHit] = []
            holds: List[OsuHold] = []

            # Note Conversion
            for hit in o2jMap.notes.hits():
                hits.append(OsuHit(offset=hit.offset, column=hit.column))
            for hold in o2jMap.notes.holds():
                holds.append(OsuHold(offset=hold.offset, column=hold.column, length=hold.length))

            bpms: List[Bpm] = []

            # Timing Point Conversion
            for bpm in o2jMap.bpms:
                bpms.append(OsuBpm(offset=bpm.offset, bpm=bpm.bpm))

            # Extract Metadata
            osuMap = OsuMap(
                title=o2j.title,
                artist=o2j.artist,
                creator=o2j.creator,
                version=f"Level {o2j.level[o2j.maps.index(o2jMap)]}",
                bpms=OsuBpmList(bpms),
                circleSize=7,
                notes=OsuNotePkg(hits=OsuHitList(hits),
                                 holds=OsuHoldList(holds))
            )
            osuMapSet.append(osuMap)
        return osuMapSet

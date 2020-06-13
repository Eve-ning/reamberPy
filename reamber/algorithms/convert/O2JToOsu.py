from reamber.o2jam.O2JMapSetObj import O2JMapSetObj, O2JMapObj
from reamber.osu.OsuMapObj import OsuMapObj
from reamber.osu.OsuHitObj import OsuHitObj
from reamber.osu.OsuHoldObj import OsuHoldObj
from reamber.osu.OsuBpmObj import OsuBpmObj
from reamber.base.BpmObj import BpmObj
from reamber.osu.lists.OsuBpmList import OsuBpmList
from reamber.osu.lists.OsuNotePkg import OsuNotePkg
from reamber.osu.lists.notes.OsuHoldList import OsuHoldList
from reamber.osu.lists.notes.OsuHitList import OsuHitList
from typing import List


class O2JToOsu:
    @staticmethod
    def convert(o2j: O2JMapSetObj) -> List[OsuMapObj]:
        """ Converts a Mapset to possibly multiple osu maps
        Note that a mapset contains maps, so a list would be expected.
        O2JMap conversion is not possible due to lack of O2JMapset Metadata
        :param o2j: The O2Jam set
        :return: Osu Map
        """

        osuMapSet: List[OsuMapObj] = []
        for o2jMap in o2j.maps:
            assert isinstance(o2jMap, O2JMapObj)

            hits: List[OsuHitObj] = []
            holds: List[OsuHoldObj] = []

            # Note Conversion
            for hit in o2jMap.notes.hits():
                hits.append(OsuHitObj(offset=hit.offset, column=hit.column))
            for hold in o2jMap.notes.holds():
                holds.append(OsuHoldObj(offset=hold.offset, column=hold.column, length=hold.length))

            bpms: List[BpmObj] = []

            # Timing Point Conversion
            for bpm in o2jMap.bpms:
                bpms.append(OsuBpmObj(offset=bpm.offset, bpm=bpm.bpm))

            # Extract Metadata
            osuMap = OsuMapObj(
                title=o2j.title,
                artist=o2j.artist,
                creator=o2j.creator,
                version=f"Level {o2j.level[o2j.maps.index(o2jm)]}",
                bpms=OsuBpmList(bpms),
                circleSize=7,
                notes=OsuNotePkg(hits=OsuHitList(hits),
                                 holds=OsuHoldList(holds))
            )
            osuMapSet.append(osuMap)
        return osuMapSet

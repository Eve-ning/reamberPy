from reamber.sm.SMMapSetObj import SMMapSetObj, SMMapObj
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


class SMToOsu:
    @staticmethod
    def convert(sm: SMMapSetObj) -> List[OsuMapObj]:
        """ Converts a SMMapset to possibly multiple osu maps

        Note that a mapset contains maps, so a list would be expected.
        SMMap conversion is not possible due to lack of SMMapset Metadata

        :param sm: The MapSet
        :return: List of Osu Maps
        """

        # I haven't tested with non 4 keys, so it might explode :(

        osuMapSet: List[OsuMapObj] = []
        for smMap in sm.maps:
            assert isinstance(smMap, SMMapObj)

            hits: List[OsuHitObj] = []
            holds: List[OsuHoldObj] = []

            # Note Conversion
            for hit in smMap.notes.hits():
                hits.append(OsuHitObj(offset=hit.offset, column=hit.column))
            for hold in smMap.notes.holds():
                holds.append(OsuHoldObj(offset=hold.offset, column=hold.column, length=hold.length))

            bpms: List[BpmObj] = []

            # Timing Point Conversion
            for bpm in smMap.bpms:
                bpms.append(OsuBpmObj(offset=bpm.offset, bpm=bpm.bpm))

            # Extract Metadata
            osuMap = OsuMapObj(
                backgroundFileName=sm.background,
                title=sm.title,
                titleUnicode=sm.titleTranslit,
                artist=sm.artist,
                artistUnicode=sm.artistTranslit,
                audioFileName=sm.music,
                creator=sm.credit,
                version=f"{smMap.difficulty} {smMap.difficultyVal}",
                previewTime=int(sm.sampleStart),
                bpms=OsuBpmList(bpms),
                notes=OsuNotePkg(hits=OsuHitList(hits),
                                 holds=OsuHoldList(holds))
            )
            osuMapSet.append(osuMap)
        return osuMapSet

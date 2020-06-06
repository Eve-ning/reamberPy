from reamber.sm.SMMapSetObject import SMMapSetObject, SMMapObject
from reamber.osu.OsuMapObject import OsuMapObject
from reamber.osu.OsuHitObject import OsuHitObject
from reamber.osu.OsuHoldObject import OsuHoldObject
from reamber.osu.OsuBpmObject import OsuBpmObject
from reamber.base.BpmObject import BpmObject
from reamber.osu.lists.OsuBpmList import OsuBpmList
from reamber.osu.lists.OsuNotePkg import OsuNotePkg
from reamber.osu.lists.notes.OsuHoldList import OsuHoldList
from reamber.osu.lists.notes.OsuHitList import OsuHitList
from typing import List


class SMToOsu:
    @staticmethod
    def convert(sm: SMMapSetObject) -> List[OsuMapObject]:
        """ Converts a Mapset to possibly multiple osu maps
        Note that a mapset contains maps, so a list would be expected.
        SMMap conversion is not possible due to lack of SMMapset Metadata
        :param sm: The MapSet
        :return: Osu Map
        """

        # I haven't tested with non 4 keys, so it might explode :(

        osuMapSet: List[OsuMapObject] = []
        for smMap in sm.maps:
            assert isinstance(smMap, SMMapObject)

            hits: List[OsuHitObject] = []
            holds: List[OsuHoldObject] = []

            # Note Conversion
            for hit in smMap.notes.hits:
                hits.append(OsuHitObject(offset=hit.offset, column=hit.column))
            for hold in smMap.notes.holds:
                holds.append(OsuHoldObject(offset=hold.offset, column=hold.column, length=hold.length))

            bpms: List[BpmObject] = []

            # Timing Point Conversion
            for bpm in smMap.bpms:
                bpms.append(OsuBpmObject(offset=bpm.offset, bpm=bpm.bpm))

            # Extract Metadata
            osuMap = OsuMapObject(
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
                notes=OsuNotePkg(OsuHitList(hits),
                                 OsuHoldList(holds))
            )
            osuMapSet.append(osuMap)
        return osuMapSet

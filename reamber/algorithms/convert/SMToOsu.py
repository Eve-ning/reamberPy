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
from reamber.sm.SMMapSet import SMMapSet, SMMap


class SMToOsu:
    OFFSET = 68

    @staticmethod
    def convert(sm: SMMapSet) -> List[OsuMap]:
        """ Converts a SMMapset to possibly multiple osu maps

        Note that a mapset contains maps, so a list would be expected.
        SMMap conversion is not possible due to lack of SMMapset Metadata

        :param sm:
        :return:
        """

        # I haven't tested with non 4 keys, so it might explode :(

        osuMapSet: List[OsuMap] = []
        for smMap in sm.maps:
            assert isinstance(smMap, SMMap)

            hits: List[OsuHit] = []
            holds: List[OsuHold] = []

            # Note Conversion
            for hit in smMap.notes.hits():
                hits.append(OsuHit(offset=hit.offset, column=hit.column))
            for hold in smMap.notes.holds():
                holds.append(OsuHold(offset=hold.offset, column=hold.column, _length=hold.length))

            bpms: List[Bpm] = []

            # Timing Point Conversion
            for bpm in smMap.bpms:
                bpms.append(OsuBpm(offset=bpm.offset, bpm=bpm.bpm))

            # Extract Metadata
            osuMap = OsuMap(
                background_file_name=sm.background,
                title=sm.title,
                title_unicode=sm.titleTranslit,
                artist=sm.artist,
                artist_unicode=sm.artistTranslit,
                audio_file_name=sm.music,
                creator=sm.credit,
                version=f"{smMap.difficulty} {smMap.difficultyVal}",
                preview_time=int(sm.sampleStart),
                bpms=OsuBpmList(bpms),
                notes=OsuNotePkg(hits=OsuHitList(hits),
                                 holds=OsuHoldList(holds))
            )
            osuMapSet.append(osuMap)
        return osuMapSet

from typing import List

from reamber.base.Bpm import Bpm
from reamber.osu.OsuBpm import OsuBpm
from reamber.osu.OsuHit import OsuHit
from reamber.osu.OsuHold import OsuHold
from reamber.osu.OsuMap import OsuMap
from reamber.osu.lists.OsuBpmList import OsuBpmList
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

        osu_map_set: List[OsuMap] = []
        for sm_map in sm.maps:
            assert isinstance(sm_map, SMMap)

            # Note Conversion
            hits = OsuHitList.empty(len(sm_map.hits))
            hits.offset = sm_map.hits.offset
            hits.column = sm_map.hits.column

            holds = OsuHoldList.empty(len(sm_map.holds))
            holds.offset = sm_map.holds.offset
            holds.column = sm_map.holds.column
            holds.length = sm_map.holds.length

            bpms = OsuBpmList.empty(len(sm_map.bpms))
            bpms.offset = sm_map.bpms.offset
            bpms.bpm = sm_map.bpms.bpm
            bpms.metronome = sm_map.bpms.metronome

            # Extract Metadata
            osuMap = OsuMap(
                background_file_name=sm.background,
                title=sm.title,
                title_unicode=sm.title_translit,
                artist=sm.artist,
                artist_unicode=sm.artist_translit,
                audio_file_name=sm.music,
                creator=sm.credit,
                version=f"{sm_map.difficulty} {sm_map.difficulty_val}",
                preview_time=int(sm.sample_start),
            )
            osuMap.hits = hits
            osuMap.holds = holds
            osuMap.bpms = bpms
            osu_map_set.append(osuMap)
        return osu_map_set

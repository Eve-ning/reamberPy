from typing import List

from reamber.base.Bpm import Bpm
from reamber.osu.OsuBpm import OsuBpm
from reamber.osu.OsuHit import OsuHit
from reamber.osu.OsuHold import OsuHold
from reamber.osu.OsuMap import OsuMap
from reamber.osu.OsuSv import OsuSv
from reamber.osu.lists.OsuBpmList import OsuBpmList
from reamber.osu.lists.OsuSvList import OsuSvList
from reamber.osu.lists.notes.OsuHitList import OsuHitList
from reamber.osu.lists.notes.OsuHoldList import OsuHoldList
from reamber.quaver.QuaMap import QuaMap
from reamber.quaver.QuaMapMeta import QuaMapMode


class QuaToOsu:
    @staticmethod
    def convert(qua: QuaMap) -> OsuMap:
        """ Converts a Quaver map to an osu map

        :param qua:
        :return:
        """

        hits: List[OsuHit] = []
        holds: List[OsuHold] = []

        # Note Conversion
        for hit in qua.notes.hits():
            hits.append(OsuHit(offset=hit.offset, column=hit.column))
        for hold in qua.notes.holds():
            holds.append(OsuHold(offset=hold.offset, column=hold.column, _length=hold.length))

        bpms: List[Bpm] = []
        svs: List[OsuSv] = []
        # Timing Point Conversion
        for bpm in qua.bpms:
            bpms.append(OsuBpm(offset=bpm.offset, bpm=bpm.bpm))

        for sv in qua.svs:
            svs.append(OsuSv(offset=sv.offset, multiplier=sv.multiplier))

        # Extract Metadata
        osuMap = OsuMap(
            background_file_name=qua.background_file,
            title=qua.title,
            circle_size=QuaMapMode.get_keys(qua.mode),
            title_unicode=qua.title,
            artist=qua.artist,
            artist_unicode=qua.artist,
            audio_file_name=qua.audio_file,
            creator=qua.creator,
            version=qua.difficulty_name,
            preview_time=qua.song_preview_time,
            bpms=OsuBpmList(bpms),
            svs=OsuSvList(svs),
            tags=qua.tags,
            notes=OsuNotePkg(hits=OsuHitList(hits),
                             holds=OsuHoldList(holds))
        )

        return osuMap

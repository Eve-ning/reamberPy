from reamber.quaver.QuaMap import QuaMap
from reamber.quaver.QuaMapMeta import QuaMapMode
from reamber.osu.OsuMap import OsuMap
from reamber.osu.OsuHit import OsuHit
from reamber.osu.OsuHold import OsuHold
from reamber.osu.OsuBpm import OsuBpm
from reamber.osu.OsuSv import OsuSv
from reamber.base.Bpm import Bpm

from reamber.osu.lists.OsuBpmList import OsuBpmList
from reamber.osu.lists.OsuNotePkg import OsuNotePkg
from reamber.osu.lists.notes.OsuHoldList import OsuHoldList
from reamber.osu.lists.notes.OsuHitList import OsuHitList
from reamber.osu.lists.OsuSvList import OsuSvList
from typing import List


class QuaToOsu:
    @staticmethod
    def convert(qua: QuaMap) -> OsuMap:
        """ Converts a Quaver map to an osu map

        :param qua: Quaver map
        :return: Osu Map
        """

        hits: List[OsuHit] = []
        holds: List[OsuHold] = []

        # Note Conversion
        for hit in qua.notes.hits():
            hits.append(OsuHit(offset=hit.offset, column=hit.column))
        for hold in qua.notes.holds():
            holds.append(OsuHold(offset=hold.offset, column=hold.column, length=hold.length))

        bpms: List[Bpm] = []
        svs: List[OsuSv] = []
        # Timing Point Conversion
        for bpm in qua.bpms:
            bpms.append(OsuBpm(offset=bpm.offset, bpm=bpm.bpm))

        for sv in qua.svs:
            svs.append(OsuSv(offset=sv.offset, multiplier=sv.multiplier))

        # Extract Metadata
        osuMap = OsuMap(
            backgroundFileName=qua.backgroundFile,
            title=qua.title,
            circleSize=QuaMapMode.keys(qua.mode),
            titleUnicode=qua.title,
            artist=qua.artist,
            artistUnicode=qua.artist,
            audioFileName=qua.audioFile,
            creator=qua.creator,
            version=qua.difficultyName,
            previewTime=qua.songPreviewTime,
            bpms=OsuBpmList(bpms),
            svs=OsuSvList(svs),
            notes=OsuNotePkg(hits=OsuHitList(hits),
                             holds=OsuHoldList(holds))
        )

        return osuMap

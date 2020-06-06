from reamber.quaver.QuaMapObject import QuaMapObject
from reamber.quaver.QuaMapObjectMeta import QuaMapObjectMode
from reamber.osu.OsuMapObject import OsuMapObject
from reamber.osu.OsuHitObject import OsuHitObject
from reamber.osu.OsuHoldObject import OsuHoldObject
from reamber.osu.OsuBpmObject import OsuBpmObject
from reamber.osu.OsuSvObject import OsuSvObject
from reamber.base.BpmObject import BpmObject

from reamber.osu.lists.OsuBpmList import OsuBpmList
from reamber.osu.lists.OsuNotePkg import OsuNotePkg
from reamber.osu.lists.notes.OsuHoldList import OsuHoldList
from reamber.osu.lists.notes.OsuHitList import OsuHitList
from reamber.osu.lists.OsuSvList import OsuSvList
from typing import List


class QuaToOsu:
    @staticmethod
    def convert(qua: QuaMapObject) -> OsuMapObject:
        """ Converts a map to an osu map
        :param qua: The Map
        :return: Osu Map
        """

        hits: List[OsuHitObject] = []
        holds: List[OsuHoldObject] = []

        # Note Conversion
        for hit in qua.notes.hits:
            hits.append(OsuHitObject(offset=hit.offset, column=hit.column))
        for hold in qua.notes.holds:
            holds.append(OsuHoldObject(offset=hold.offset, column=hold.column, length=hold.length))

        bpms: List[BpmObject] = []
        svs: List[OsuSvObject] = []
        # Timing Point Conversion
        for bpm in qua.bpms:
            bpms.append(OsuBpmObject(offset=bpm.offset, bpm=bpm.bpm))

        for sv in qua.svs:
            svs.append(OsuSvObject(offset=sv.offset, multiplier=sv.multiplier))

        # Extract Metadata
        osuMap = OsuMapObject(
            backgroundFileName=qua.backgroundFile,
            title=qua.title,
            circleSize=QuaMapObjectMode.keys(qua.mode),
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

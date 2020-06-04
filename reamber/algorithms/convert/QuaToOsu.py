from reamber.quaver.QuaMapObject import QuaMapObject
from reamber.quaver.QuaMapObjectMeta import QuaMapObjectMode
from reamber.osu.OsuMapObject import OsuMapObject
from reamber.osu.OsuHitObject import OsuHitObject
from reamber.osu.OsuHoldObject import OsuHoldObject
from reamber.osu.OsuBpmPoint import OsuBpmPoint
from reamber.osu.OsuSliderVelocity import OsuSliderVelocity
from reamber.base.BpmPoint import BpmPoint

from reamber.osu.mapobj.OsuMapObjectBpms import OsuMapObjectBpms
from reamber.osu.mapobj.OsuMapObjectNotes import OsuMapObjectNotes
from reamber.osu.mapobj.notes.OsuMapObjectHolds import OsuMapObjectHolds
from reamber.osu.mapobj.notes.OsuMapObjectHits import OsuMapObjectHits
from reamber.osu.mapobj.OsuMapObjectSvs import OsuMapObjectSvs
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

        bpms: List[BpmPoint] = []
        svs: List[OsuSliderVelocity] = []
        # Timing Point Conversion
        for bpm in qua.bpms:
            bpms.append(OsuBpmPoint(offset=bpm.offset, bpm=bpm.bpm))

        for sv in qua.svs:
            svs.append(OsuSliderVelocity(offset=sv.offset, multiplier=sv.multiplier))

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
            bpms=OsuMapObjectBpms(bpms),
            svs=OsuMapObjectSvs(svs),
            notes=OsuMapObjectNotes(hits=OsuMapObjectHits(hits),
                                    holds=OsuMapObjectHolds(holds))
        )

        return osuMap

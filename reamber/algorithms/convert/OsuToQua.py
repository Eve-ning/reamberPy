from reamber.quaver.QuaMapObject import QuaMapObject
from reamber.quaver.QuaMapObjectMeta import QuaMapObjectMode
from reamber.quaver.QuaSliderVelocity import QuaSliderVelocity
from reamber.osu.OsuMapObject import OsuMapObject
from reamber.base.BpmPoint import BpmPoint
from reamber.quaver.QuaHitObject import QuaHitObject
from reamber.quaver.QuaHoldObject import QuaHoldObject
from reamber.quaver.QuaBpmPoint import QuaBpmPoint
from reamber.quaver.mapobj import QuaMapObjectBpms
from reamber.quaver.mapobj import QuaMapObjectNotes
from reamber.quaver.mapobj import QuaMapObjectSvs
from reamber.quaver.mapobj.notes.QuaMapObjectHits import QuaMapObjectHits
from reamber.quaver.mapobj.notes.QuaMapObjectHolds import QuaMapObjectHolds
from typing import List


class OsuToQua:
    @staticmethod
    def convert(osu: OsuMapObject) -> QuaMapObject:
        """ Converts Osu to a Qua Map
        :param osu: The Osu Map itself
        :return: A SM MapSet
        """
        assert osu.circleSize == 4 or osu.circleSize == 7

        hits: List[QuaHitObject] = []
        holds: List[QuaHoldObject] = []

        for hit in osu.notes.hits:
            hits.append(QuaHitObject(offset=hit.offset, column=hit.column))
        for hold in osu.notes.holds:
            holds.append(QuaHoldObject(offset=hold.offset, column=hold.column, length=hold.length))

        bpms: List[BpmPoint] = []
        svs: List[QuaSliderVelocity] = []

        for bpm in osu.bpms:
            bpms.append(QuaBpmPoint(offset=bpm.offset, bpm=bpm.bpm))

        for sv in osu.svs:
            svs.append(QuaSliderVelocity(offset=sv.offset, multiplier=sv.multiplier))

        qua: QuaMapObject = QuaMapObject(
            audioFile=osu.audioFileName,
            title=osu.titleUnicode,
            mode=QuaMapObjectMode.str(int(osu.circleSize)),
            artist=osu.artistUnicode,
            creator=osu.creator,
            backgroundFile=osu.backgroundFileName,
            songPreviewTime=osu.previewTime,
            notes=QuaMapObjectNotes(hits=QuaMapObjectHits(hits), holds=QuaMapObjectHolds(holds)),
            bpms=QuaMapObjectBpms(bpms),
            svs=QuaMapObjectSvs(svs)
        )

        return qua

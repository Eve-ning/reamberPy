from reamber.quaver.QuaMapObject import QuaMapObject
from reamber.quaver.QuaMapObjectMeta import QuaMapObjectMode
from reamber.quaver.QuaSvObject import QuaSvObject
from reamber.osu.OsuMapObject import OsuMapObject
from reamber.base.BpmObject import BpmObject
from reamber.quaver.QuaHitObject import QuaHitObject
from reamber.quaver.QuaHoldObject import QuaHoldObject
from reamber.quaver.QuaBpmObject import QuaBpmObject
from reamber.quaver.lists import QuaBpmList
from reamber.quaver.lists import QuaNotePkg
from reamber.quaver.lists import QuaSvList
from reamber.quaver.lists.notes.QuaHitList import QuaHitList
from reamber.quaver.lists.notes.QuaHoldList import QuaHoldList
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

        bpms: List[BpmObject] = []
        svs: List[QuaSvObject] = []

        for bpm in osu.bpms:
            bpms.append(QuaBpmObject(offset=bpm.offset, bpm=bpm.bpm))

        for sv in osu.svs:
            svs.append(QuaSvObject(offset=sv.offset, multiplier=sv.multiplier))

        qua: QuaMapObject = QuaMapObject(
            audioFile=osu.audioFileName,
            title=osu.titleUnicode,
            mode=QuaMapObjectMode.str(int(osu.circleSize)),
            artist=osu.artistUnicode,
            creator=osu.creator,
            backgroundFile=osu.backgroundFileName,
            songPreviewTime=osu.previewTime,
            notes=QuaNotePkg(hits=QuaHitList(hits), holds=QuaHoldList(holds)),
            bpms=QuaBpmList(bpms),
            svs=QuaSvList(svs)
        )

        return qua

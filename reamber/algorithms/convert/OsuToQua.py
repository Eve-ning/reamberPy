from reamber.quaver.QuaMapObj import QuaMapObj
from reamber.quaver.QuaMapObjMeta import QuaMapObjMode
from reamber.quaver.QuaSvObj import QuaSvObj
from reamber.osu.OsuMapObj import OsuMapObj
from reamber.base.BpmObj import BpmObj
from reamber.quaver.QuaHitObj import QuaHitObj
from reamber.quaver.QuaHoldObj import QuaHoldObj
from reamber.quaver.QuaBpmObj import QuaBpmObj
from reamber.quaver.lists import QuaBpmList
from reamber.quaver.lists import QuaNotePkg
from reamber.quaver.lists import QuaSvList
from reamber.quaver.lists.notes.QuaHitList import QuaHitList
from reamber.quaver.lists.notes.QuaHoldList import QuaHoldList
from typing import List


class OsuToQua:
    @staticmethod
    def convert(osu: OsuMapObj) -> QuaMapObj:
        """ Converts Osu to a Qua Map
        :param osu: The Osu Map itself
        :return: A SM MapSet
        """
        assert osu.circleSize == 4 or osu.circleSize == 7

        hits: List[QuaHitObj] = []
        holds: List[QuaHoldObj] = []

        for hit in osu.notes.hits():
            hits.append(QuaHitObj(offset=hit.offset, column=hit.column))
        for hold in osu.notes.holds():
            holds.append(QuaHoldObj(offset=hold.offset, column=hold.column, length=hold.length))

        bpms: List[BpmObj] = []
        svs: List[QuaSvObj] = []

        for bpm in osu.bpms:
            bpms.append(QuaBpmObj(offset=bpm.offset, bpm=bpm.bpm))

        for sv in osu.svs:
            svs.append(QuaSvObj(offset=sv.offset, multiplier=sv.multiplier))

        qua: QuaMapObj = QuaMapObj(
            audioFile=osu.audioFileName,
            title=osu.titleUnicode,
            mode=QuaMapObjMode.str(int(osu.circleSize)),
            artist=osu.artistUnicode,
            creator=osu.creator,
            backgroundFile=osu.backgroundFileName,
            songPreviewTime=osu.previewTime,
            notes=QuaNotePkg(hits=QuaHitList(hits),
                             holds=QuaHoldList(holds)),
            bpms=QuaBpmList(bpms),
            svs=QuaSvList(svs)
        )

        return qua

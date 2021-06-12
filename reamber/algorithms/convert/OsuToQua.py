from typing import List

from reamber.base.Bpm import Bpm
from reamber.osu.OsuMap import OsuMap
from reamber.quaver.QuaBpm import QuaBpm
from reamber.quaver.QuaHit import QuaHit
from reamber.quaver.QuaHold import QuaHold
from reamber.quaver.QuaMap import QuaMap
from reamber.quaver.QuaMapMeta import QuaMapMode
from reamber.quaver.QuaSv import QuaSv
from reamber.quaver.lists import QuaBpmList
from reamber.quaver.lists import QuaNotePkg
from reamber.quaver.lists import QuaSvList
from reamber.quaver.lists.notes.QuaHitList import QuaHitList
from reamber.quaver.lists.notes.QuaHoldList import QuaHoldList


class OsuToQua:
    @staticmethod
    def convert(osu: OsuMap, assertKeys=True) -> QuaMap:
        """ Converts Osu to a Qua Map

        :param osu:
        :param assertKeys: Adds an assertion to verify that Quaver can support this key mode
        :return:
        """
        if assertKeys: assert QuaMapMode.getMode(int(osu.circleSize)) != "",\
            "Current Circle Size (Keys) is not supported"

        hits: List[QuaHit] = []
        holds: List[QuaHold] = []

        for hit in osu.notes.hits():
            hits.append(QuaHit(offset=int(hit.offset), column=hit.column))
        for hold in osu.notes.holds():
            holds.append(QuaHold(offset=int(hold.offset), column=hold.column, _length=int(hold.length)))

        bpms: List[Bpm] = []
        svs: List[QuaSv] = []

        for bpm in osu.bpms:
            bpms.append(QuaBpm(offset=bpm.offset, bpm=bpm.bpm))

        for sv in osu.svs:
            svs.append(QuaSv(offset=sv.offset, multiplier=sv.multiplier))

        qua: QuaMap = QuaMap(
            audioFile=osu.audioFileName,
            title=osu.titleUnicode,
            mode=QuaMapMode.getMode(int(osu.circleSize)),
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

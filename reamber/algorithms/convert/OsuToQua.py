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
        if assertKeys: assert QuaMapMode.get_mode(int(osu.circle_size)) != "",\
            "Current Circle Size (Keys) is not supported"

        hits: List[QuaHit] = []
        holds: List[QuaHold] = []

        for hit in osu.notes.hits():
            hits.append(QuaHit(offset=hit.offset, column=hit.column))
        for hold in osu.notes.holds():
            holds.append(QuaHold(offset=hold.offset, column=hold.column, _length=hold.length))

        bpms: List[Bpm] = []
        svs: List[QuaSv] = []

        for bpm in osu.bpms:
            bpms.append(QuaBpm(offset=bpm.offset, bpm=bpm.bpm))

        for sv in osu.svs:
            svs.append(QuaSv(offset=sv.offset, multiplier=sv.multiplier))

        qua: QuaMap = QuaMap(
            audio_file=osu.audio_file_name,
            title=osu.title_unicode,
            mode=QuaMapMode.get_mode(int(osu.circle_size)),
            artist=osu.artist_unicode,
            creator=osu.creator,
            tags=osu.tags,
            difficulty_name=osu.version,
            background_file=osu.background_file_name,
            song_preview_time=osu.preview_time,
            notes=QuaNotePkg(hits=QuaHitList(hits),
                             holds=QuaHoldList(holds)),
            bpms=QuaBpmList(bpms),
            svs=QuaSvList(svs)
        )

        return qua

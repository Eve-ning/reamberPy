from typing import List

from reamber.base.Bpm import Bpm
from reamber.osu.OsuMap import OsuMap
from reamber.sm.SMBpm import SMBpm
from reamber.sm.SMHit import SMHit
from reamber.sm.SMHold import SMHold
from reamber.sm.SMMapMeta import SMMapChartTypes
from reamber.sm.SMMapSet import SMMapSet, SMMap
from reamber.sm.lists.SMBpmList import SMBpmList
from reamber.sm.lists.SMNotePkg import SMNotePkg
from reamber.sm.lists.notes.SMHitList import SMHitList
from reamber.sm.lists.notes.SMHoldList import SMHoldList


class OsuToSM:
    OFFSET = 68

    @staticmethod
    def convert(osu: OsuMap, assertKeys=True) -> SMMapSet:
        """ Converts Osu to a SMMapset Obj

        Note that each osu map object will create a separate mapset, they are not merged

        :param osu:
        :param assertKeys: Adds an assertion to verify that Quaver can support this key mode
        :return:
        """

        if assertKeys: assert osu.circle_size == 4

        hits: List[SMHit] = []
        holds: List[SMHold] = []

        for hit in osu.notes.hits():
            hits.append(SMHit(offset=hit.offset, column=hit.column))
        for hold in osu.notes.holds():
            holds.append(SMHold(offset=hold.offset, column=hold.column, _length=hold.length))

        bpms: List[Bpm] = []

        for bpm in osu.bpms:
            bpms.append(SMBpm(offset=bpm.offset, bpm=bpm.bpm))

        smSet: SMMapSet = SMMapSet(
            music=osu.audio_file_name,
            title=osu.title,
            titleTranslit=osu.title_unicode,
            artist=osu.artist,
            artistTranslit=osu.artist_unicode,
            credit=osu.creator,
            background=osu.background_file_name,
            sampleStart=osu.preview_time,
            sampleLength=10,
            offset=-OsuToSM.OFFSET,
            maps=[
                SMMap(
                    chartType=SMMapChartTypes.DANCE_SINGLE,
                    notes=SMNotePkg(hits=SMHitList(hits),
                                    holds=SMHoldList(holds)),
                    bpms=SMBpmList(bpms)
                )
            ]
        )

        return smSet

from reamber.sm.SMMapSet import SMMapSet, SMMap
from reamber.osu.OsuMap import OsuMap
from reamber.base.Bpm import Bpm
from reamber.sm.SMMapMeta import SMMapChartTypes
from reamber.sm.SMHit import SMHit
from reamber.sm.SMHold import SMHold
from reamber.sm.SMBpm import SMBpm
from reamber.sm.lists.SMNotePkg import SMNotePkg
from reamber.sm.lists.SMBpmList import SMBpmList
from reamber.sm.lists.notes.SMHitList import SMHitList
from reamber.sm.lists.notes.SMHoldList import SMHoldList
from typing import List


class OsuToSM:
    @staticmethod
    def convert(osu: OsuMap) -> SMMapSet:
        """ Converts Osu to a SMMapset Obj

        Note that each osu map object will create a separate mapset, they are not merged

        :param osu: Osu Map
        :return: SM Mapset
        """

        # I haven't tested with non 4 keys, so it might explode :(

        assert osu.circleSize == 4

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
            music=osu.audioFileName,
            title=osu.title,
            titleTranslit=osu.titleUnicode,
            artist=osu.artist,
            artistTranslit=osu.artistUnicode,
            credit=osu.creator,
            background=osu.backgroundFileName,
            sampleStart=osu.previewTime,
            sampleLength=10,
            offset=osu.notes.firstOffset(),
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

from reamber.sm.SMMapSetObj import SMMapSetObj, SMMapObj
from reamber.osu.OsuMapObj import OsuMapObj
from reamber.base.BpmObj import BpmObj
from reamber.sm.SMMapObjMeta import SMMapObjChartTypes
from reamber.sm.SMHitObj import SMHitObj
from reamber.sm.SMHoldObj import SMHoldObj
from reamber.sm.SMBpmObj import SMBpmObj
from reamber.sm.lists.SMNotePkg import SMNotePkg
from reamber.sm.lists.SMBpmList import SMBpmList
from reamber.sm.lists.notes.SMHitList import SMHitList
from reamber.sm.lists.notes.SMHoldList import SMHoldList
from typing import List


class OsuToSM:
    @staticmethod
    def convert(osu: OsuMapObj) -> SMMapSetObj:
        """ Converts Osu to a SMMapset Obj

        Note that each osu map object will create a separate mapset, they are not merged

        :param osu: Osu Map
        :return: SM Mapset
        """

        # I haven't tested with non 4 keys, so it might explode :(

        assert osu.circleSize == 4

        hits: List[SMHitObj] = []
        holds: List[SMHoldObj] = []

        for hit in osu.notes.hits():
            hits.append(SMHitObj(offset=hit.offset, column=hit.column))
        for hold in osu.notes.holds():
            holds.append(SMHoldObj(offset=hold.offset, column=hold.column, length=hold.length))

        bpms: List[BpmObj] = []

        for bpm in osu.bpms:
            bpms.append(SMBpmObj(offset=bpm.offset, bpm=bpm.bpm))

        smSet: SMMapSetObj = SMMapSetObj(
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
                SMMapObj(
                    chartType=SMMapObjChartTypes.DANCE_SINGLE,
                    notes=SMNotePkg(hits=SMHitList(hits),
                                    holds=SMHoldList(holds)),
                    bpms=SMBpmList(bpms)
                )
            ]
        )

        return smSet

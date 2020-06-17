from reamber.sm.SMMapSetObj import SMMapSetObj, SMMapObj
from reamber.quaver.QuaMapObj import QuaMapObj
from reamber.base.BpmObj import BpmObj
from reamber.sm.SMMapObjMeta import SMMapObjChartTypes
from reamber.sm.SMHitObj import SMHitObj
from reamber.sm.SMHoldObj import SMHoldObj
from reamber.sm.SMBpmObj import SMBpmObj
from reamber.sm.lists.SMBpmList import SMBpmList
from reamber.sm.lists.SMNotePkg import SMNotePkg
from reamber.sm.lists.notes.SMHitList import SMHitList
from reamber.sm.lists.notes.SMHoldList import SMHoldList
from typing import List


class QuaToSM:
    @staticmethod
    def convert(qua: QuaMapObj) -> SMMapSetObj:
        """ Converts a Quaver map to a SMMapset Obj

        Note that each qua map object will create a separate mapset, they are not merged

        :param qua: Quaver map
        :return: SM Mapset
        """
        hits: List[SMHitObj] = []
        holds: List[SMHoldObj] = []

        for hit in qua.notes.hits():
            hits.append(SMHitObj(offset=hit.offset, column=hit.column))
        for hold in qua.notes.holds():
            holds.append(SMHoldObj(offset=hold.offset, column=hold.column, length=hold.length))

        bpms: List[BpmObj] = []

        for bpm in qua.bpms:
            bpms.append(SMBpmObj(offset=bpm.offset, bpm=bpm.bpm))

        smSet: SMMapSetObj = SMMapSetObj(
            music=qua.audioFile,
            title=qua.title,
            titleTranslit=qua.title,
            artist=qua.artist,
            artistTranslit=qua.artist,
            credit=qua.creator,
            background=qua.backgroundFile,
            sampleStart=qua.songPreviewTime,
            sampleLength=10,
            offset=qua.notes.firstOffset(),
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

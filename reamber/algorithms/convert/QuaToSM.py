from reamber.sm.SMMapSetObject import SMMapSetObject, SMMapObject
from reamber.quaver.QuaMapObject import QuaMapObject
from reamber.base.BpmPoint import BpmPoint
from reamber.sm.SMMapObjectMeta import SMMapObjectChartTypes
from reamber.sm.SMHitObject import SMHitObject
from reamber.sm.SMHoldObject import SMHoldObject
from reamber.sm.SMBpmPoint import SMBpmPoint
from reamber.sm.mapobj.SMMapObjectBpms import SMMapObjectBpms
from reamber.sm.mapobj.SMMapObjectNotes import SMMapObjectNotes
from reamber.sm.mapobj.notes.SMMapObjectHits import SMMapObjectHits
from reamber.sm.mapobj.notes.SMMapObjectHolds import SMMapObjectHolds
from typing import List


class QuaToSM:
    @staticmethod
    def convert(qua: QuaMapObject) -> SMMapSetObject:
        """ Converts Osu to a SMMapset Object
        Note that each qua map object will create a separate mapset, they are not merged
        :param qua: The Quaver Map itself
        :return: A SM MapSet
        """
        hits: List[SMHitObject] = []
        holds: List[SMHoldObject] = []

        for hit in qua.notes.hits:
            hits.append(SMHitObject(offset=hit.offset, column=hit.column))
        for hold in qua.notes.holds:
            holds.append(SMHoldObject(offset=hold.offset, column=hold.column, length=hold.length))

        bpms: List[BpmPoint] = []

        for bpm in qua.bpms:
            bpms.append(SMBpmPoint(offset=bpm.offset, bpm=bpm.bpm))

        smSet: SMMapSetObject = SMMapSetObject(
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
                SMMapObject(
                    chartType=SMMapObjectChartTypes.DANCE_SINGLE,
                    notes=SMMapObjectNotes(hits=SMMapObjectHits(hits),
                                           holds=SMMapObjectHolds(holds)),
                    bpms=SMMapObjectBpms(bpms)
                )
            ]
        )

        return smSet

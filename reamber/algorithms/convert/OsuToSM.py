from reamber.sm.SMMapSetObject import SMMapSetObject, SMMapObject
from reamber.osu.OsuMapObject import OsuMapObject
from reamber.base.BpmPoint import BpmPoint
from reamber.sm.SMMapObjectMeta import SMMapObjectChartTypes
from reamber.sm.SMHitObject import SMHitObject
from reamber.sm.SMHoldObject import SMHoldObject
from reamber.sm.SMBpmPoint import SMBpmPoint
from reamber.sm.mapobj.SMMapObjectNotes import SMMapObjectNotes
from reamber.sm.mapobj.SMMapObjectBpms import SMMapObjectBpms
from reamber.sm.mapobj.notes.SMMapObjectHits import SMMapObjectHits
from reamber.sm.mapobj.notes.SMMapObjectHolds import SMMapObjectHolds
from typing import List


class OsuToSM:
    @staticmethod
    def convert(osu: OsuMapObject) -> SMMapSetObject:
        """ Converts Osu to a SMMapset Object
        Note that each osu map object will create a separate mapset, they are not merged
        :param osu: The Osu Map itself
        :return: A SM MapSet
        """

        # I haven't tested with non 4 keys, so it might explode :(

        assert osu.circleSize == 4

        hits: List[SMHitObject] = []
        holds: List[SMHoldObject] = []

        for hit in osu.notes.hits:
            hits.append(SMHitObject(offset=hit.offset, column=hit.column))
        for hold in osu.notes.holds:
            holds.append(SMHoldObject(offset=hold.offset, column=hold.column, length=hold.length))

        bpms: List[BpmPoint] = []

        for bpm in osu.bpms:
            bpms.append(SMBpmPoint(offset=bpm.offset, bpm=bpm.bpm))

        smSet: SMMapSetObject = SMMapSetObject(
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
                SMMapObject(
                    chartType=SMMapObjectChartTypes.DANCE_SINGLE,
                    notes=SMMapObjectNotes(hits=SMMapObjectHits(hits),
                                           holds=SMMapObjectHolds(holds)),
                    bpms=SMMapObjectBpms(bpms)
                )
            ]
        )

        return smSet

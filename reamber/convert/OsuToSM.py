from reamber.sm.SMMapSetObject import SMMapSetObject, SMMapObject
from reamber.osu.OsuMapObject import OsuMapObject
from reamber.base.BpmPoint import BpmPoint
from reamber.base.NoteObject import NoteObject
from reamber.sm.SMMapObjectMeta import SMMapObjectChartTypes
from reamber.sm.SMHitObject import SMHitObject
from reamber.sm.SMHoldObject import SMHoldObject
from reamber.sm.SMBpmPoint import SMBpmPoint
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

        notes: List[NoteObject] = []

        for note in osu.hitObjects():
            notes.append(SMHitObject(offset=note.offset, column=note.column))
        for note in osu.holdObjects():
            notes.append(SMHoldObject(offset=note.offset, column=note.column, length=note.length))

        bpms: List[BpmPoint] = []

        for bpm in osu.bpmPoints:
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
            offset=osu.firstNoteOffset(),
            maps=[
                SMMapObject(
                    chartType=SMMapObjectChartTypes.DANCE_SINGLE,
                    noteObjects=notes,
                    bpmPoints=bpms
                )
            ]
        )

        return smSet

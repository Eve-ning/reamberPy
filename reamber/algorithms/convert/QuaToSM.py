from reamber.sm.SMMapSetObject import SMMapSetObject, SMMapObject
from reamber.quaver.QuaMapObject import QuaMapObject
from reamber.base.BpmPoint import BpmPoint
from reamber.base.NoteObject import NoteObject
from reamber.sm.SMMapObjectMeta import SMMapObjectChartTypes
from reamber.sm.SMHitObject import SMHitObject
from reamber.sm.SMHoldObject import SMHoldObject
from reamber.sm.SMBpmPoint import SMBpmPoint
from typing import List


class QuaToSM:
    @staticmethod
    def convert(qua: QuaMapObject) -> SMMapSetObject:
        """ Converts Osu to a SMMapset Object
        Note that each qua map object will create a separate mapset, they are not merged
        :param qua: The Quaver Map itself
        :return: A SM MapSet
        """
        notes: List[NoteObject] = []

        for note in qua.hitObjects():
            notes.append(SMHitObject(offset=note.offset, column=note.column))
        for note in qua.holdObjects():
            notes.append(SMHoldObject(offset=note.offset, column=note.column, length=note.length))

        bpms: List[BpmPoint] = []

        for bpm in qua.bpmPoints:
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
            offset=qua.firstNoteOffset(),
            maps=[
                SMMapObject(
                    chartType=SMMapObjectChartTypes.DANCE_SINGLE,
                    noteObjects=notes,
                    bpmPoints=bpms
                )
            ]
        )

        return smSet

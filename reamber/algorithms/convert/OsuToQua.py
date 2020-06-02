from reamber.quaver.QuaMapObject import QuaMapObject
from reamber.quaver.QuaMapObjectMeta import QuaMapObjectMode
from reamber.quaver.QuaSliderVelocity import QuaSliderVelocity
from reamber.osu.OsuMapObject import OsuMapObject
from reamber.base.BpmPoint import BpmPoint
from reamber.base.NoteObject import NoteObject
from reamber.quaver.QuaHitObject import QuaHitObject
from reamber.quaver.QuaHoldObject import QuaHoldObject
from reamber.quaver.QuaBpmPoint import QuaBpmPoint
from typing import List


class OsuToQua:
    @staticmethod
    def convert(osu: OsuMapObject) -> QuaMapObject:
        """ Converts Osu to a Qua Map
        :param osu: The Osu Map itself
        :return: A SM MapSet
        """
        assert osu.circleSize == 4 or osu.circleSize == 7
        notes: List[NoteObject] = []

        for note in osu.notes.hitObjects():
            notes.append(QuaHitObject(offset=note.offset, column=note.column))
        for note in osu.notes.holdObjects():
            notes.append(QuaHoldObject(offset=note.offset, column=note.column, length=note.length))

        bpms: List[BpmPoint] = []
        svs: List[QuaSliderVelocity] = []

        for bpm in osu.bpms:
            bpms.append(QuaBpmPoint(offset=bpm.offset, bpm=bpm.bpm))

        for sv in osu.svPoints:
            svs.append(QuaSliderVelocity(offset=sv.offset, multiplier=sv.velocity))

        qua: QuaMapObject = QuaMapObject(
            audioFile=osu.audioFileName,
            title=osu.titleUnicode,
            mode=QuaMapObjectMode.str(int(osu.circleSize)),
            artist=osu.artistUnicode,
            creator=osu.creator,
            backgroundFile=osu.backgroundFileName,
            songPreviewTime=osu.previewTime,
            notes=notes,
            bpms=bpms,
            svPoints=svs
        )

        return qua

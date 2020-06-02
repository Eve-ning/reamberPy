from reamber.quaver.QuaMapObject import QuaMapObject
from reamber.quaver.QuaMapObjectMeta import QuaMapObjectMode
from reamber.osu.OsuMapObject import OsuMapObject
from reamber.osu.OsuHitObject import OsuHitObject
from reamber.osu.OsuHoldObject import OsuHoldObject
from reamber.osu.OsuBpmPoint import OsuBpmPoint
from reamber.osu.OsuSliderVelocity import OsuSliderVelocity
from reamber.base.BpmPoint import BpmPoint
from reamber.base.NoteObject import NoteObject
from typing import List


class QuaToOsu:
    @staticmethod
    def convert(qua: QuaMapObject):
        """ Converts a map to an osu map
        :param qua: The Map
        :return: Osu Map
        """

        notes: List[NoteObject] = []

        # Note Conversion
        for note in qua.hitObjects():
            notes.append(OsuHitObject(offset=note.offset, column=note.column))
        for note in qua.holdObjects():
            notes.append(OsuHoldObject(offset=note.offset, column=note.column, length=note.length))

        bpms: List[BpmPoint] = []
        svs: List[OsuSliderVelocity] = []
        # Timing Point Conversion
        for bpm in qua.bpmPoints:
            bpms.append(OsuBpmPoint(offset=bpm.offset, bpm=bpm.bpm))

        for sv in qua.svPoints:
            svs.append(OsuSliderVelocity(offset=sv.offset, velocity=sv.multiplier))

        # Extract Metadata
        osuMap = OsuMapObject(
            backgroundFileName=qua.backgroundFile,
            title=qua.title,
            circleSize=QuaMapObjectMode.keys(qua.mode),
            titleUnicode=qua.title,
            artist=qua.artist,
            artistUnicode=qua.artist,
            audioFileName=qua.audioFile,
            creator=qua.creator,
            version=qua.difficultyName,
            previewTime=qua.songPreviewTime,
            bpmPoints=bpms,
            svPoints=svs,
            noteObjects=notes
        )


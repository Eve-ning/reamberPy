from reamber.sm.SMMapSetObject import SMMapSetObject, SMMapObject
from reamber.quaver.QuaMapObject import QuaMapObject
from reamber.quaver.QuaHitObject import QuaHitObject
from reamber.quaver.QuaHoldObject import QuaHoldObject
from reamber.quaver.QuaBpmPoint import QuaBpmPoint
from reamber.base.BpmPoint import BpmPoint
from reamber.base.NoteObject import NoteObject
from typing import List


class SMToQua:
    @staticmethod
    def convert(sm: SMMapSetObject) -> List[QuaMapObject]:
        """ Converts a Mapset to possibly multiple quaver maps
        Note that a mapset contains maps, so a list would be expected.
        SMMap conversion is not possible due to lack of SMMapset Metadata
        :param sm: The MapSet
        :return: Quaver Maps
        """
        quaMapSet: List[QuaMapObject] = []
        for smMap in sm.maps:
            assert isinstance(smMap, SMMapObject)
            notes: List[NoteObject] = []

            # Note Conversion
            for note in smMap.hitObjects():
                notes.append(QuaHitObject(offset=note.offset, column=note.column))
            for note in smMap.holdObjects():
                notes.append(QuaHoldObject(offset=note.offset, column=note.column, length=note.length))

            bpms: List[BpmPoint] = []

            # Timing Point Conversion
            for bpm in smMap.bpmPoints:
                bpms.append(QuaBpmPoint(offset=bpm.offset, bpm=bpm.bpm))

            # Extract Metadata
            osuMap = QuaMapObject(
                backgroundFile=sm.background,
                title=sm.title,
                artist=sm.artist,
                audioFile=sm.music,
                creator=sm.credit,
                difficultyName=f"{smMap.difficulty} {smMap.difficultyVal}",
                songPreviewTime=int(sm.sampleStart),
                bpmPoints=bpms,
                noteObjects=notes
            )
            quaMapSet.append(osuMap)
        return quaMapSet


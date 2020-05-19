from reamber.sm.SMMapSetObject import SMMapSetObject, SMMapObject
from reamber.osu.OsuMapObject import OsuMapObject
from reamber.osu.OsuHitObject import OsuHitObject
from reamber.osu.OsuHoldObject import OsuHoldObject
from reamber.osu.OsuBpmPoint import OsuBpmPoint
from reamber.base.BpmPoint import BpmPoint
from reamber.base.NoteObject import NoteObject
from typing import List


class SMToOsu:
    @staticmethod
    def convert(sm: SMMapSetObject) -> List[OsuMapObject]:
        """ Converts a Mapset to possibly multiple osu maps
        Note that a mapset contains maps, so a list would be expected.
        SMMap conversion is not possible due to lack of SMMapset Metadata
        :param sm: The MapSet
        :return: Osu Map
        """
        osuMapSet: List[OsuMapObject] = []
        for smMap in sm.maps:
            assert isinstance(smMap, SMMapObject)
            notes: List[NoteObject] = []

            # Note Conversion
            for note in smMap.hitObjects():
                notes.append(OsuHitObject(offset=note.offset, column=note.column))
            for note in smMap.holdObjects():
                notes.append(OsuHoldObject(offset=note.offset, column=note.column, length=note.length))

            bpms: List[BpmPoint] = []

            # Timing Point Conversion
            for bpm in smMap.bpmPoints:
                bpms.append(OsuBpmPoint(offset=bpm.offset, bpm=bpm.bpm))

            # Extract Metadata
            osuMap = OsuMapObject(
                backgroundFileName=sm.background,
                title=sm.title,
                titleUnicode=sm.titleTranslit,
                artist=sm.artist,
                artistUnicode=sm.artistTranslit,
                audioFileName=sm.music,
                creator=sm.credit,
                version=f"{smMap.difficulty} {smMap.difficultyVal}",
                previewTime=int(sm.sampleStart),
                bpmPoints=bpms,
                noteObjects=notes
            )
            osuMapSet.append(osuMap)
        return osuMapSet


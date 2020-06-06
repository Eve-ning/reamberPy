from reamber.base.lists.notes.NoteList import NoteList
from typing import List, Type
from abc import ABC

from reamber.osu.OsuNoteObjMeta import OsuNoteObjMeta
from reamber.osu.OsuSampleSet import OsuSampleSet


class OsuNoteList(NoteList, ABC):
    def data(self) -> List[Type[OsuNoteObjMeta]]: pass

    def volumes(self) -> List[float]:
        return self.attributes('volumes')

    def hitsoundFiles(self) -> List[str]:
        return self.attributes('hitsoundFile')

    def sampleSets(self) -> List[OsuSampleSet]:
        return self.attributes('sampleSet')

    def hitsoundSets(self) -> List[OsuSampleSet]:
        return self.attributes('hitsoundSet')

    def customSets(self) -> List[OsuSampleSet]:
        return self.attributes('customSet')

    def additionSets(self) -> List[OsuSampleSet]:
        return self.attributes('additionSet')

from reamber.base.lists.notes.NoteList import NoteList
from typing import List, Type
from abc import ABC

from reamber.osu.OsuNoteMeta import OsuNoteMeta
from reamber.osu.OsuSampleSet import OsuSampleSet


class OsuNoteList(NoteList, ABC):
    def data(self) -> List[Type[OsuNoteMeta]]: pass

    def volumes(self) -> List[float]:
        return self.attribute('volume')

    def hitsoundFiles(self) -> List[str]:
        return self.attribute('hitsoundFile')

    def sampleSets(self) -> List[OsuSampleSet]:
        return self.attribute('sampleSet')

    def hitsoundSets(self) -> List[OsuSampleSet]:
        return self.attribute('hitsoundSet')

    def customSets(self) -> List[OsuSampleSet]:
        return self.attribute('customSet')

    def additionSets(self) -> List[OsuSampleSet]:
        return self.attribute('additionSet')

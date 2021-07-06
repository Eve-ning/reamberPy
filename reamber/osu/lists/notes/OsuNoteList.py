from abc import ABC
from typing import List, Type

from reamber.base.lists.notes.NoteList import NoteList
from reamber.osu.OsuNoteMeta import OsuNoteMeta
from reamber.osu.OsuSampleSet import OsuSampleSet


class OsuNoteList(NoteList, ABC):
    def data(self) -> List[Type[OsuNoteMeta]]: pass

    def volumes(self) -> List[float]:
        return self.attribute('volume')

    def hitsound_files(self) -> List[str]:
        return self.attribute('hitsound_file')

    def sample_sets(self) -> List[OsuSampleSet]:
        return self.attribute('sameple_set')

    def hitsound_sets(self) -> List[OsuSampleSet]:
        return self.attribute('hitsound_set')

    def custom_sets(self) -> List[OsuSampleSet]:
        return self.attribute('custom_set')

    def addition_sets(self) -> List[OsuSampleSet]:
        return self.attribute('addition_set')

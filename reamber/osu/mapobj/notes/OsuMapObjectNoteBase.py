from reamber.base.mapobj.notes.MapObjectNoteBase import MapObjectNoteBase
from typing import TYPE_CHECKING, List, Type
from abc import abstractmethod, ABC

from reamber.osu.OsuNoteObjectMeta import OsuNoteObjectMeta
from reamber.osu.OsuSampleSet import OsuSampleSet


class OsuMapObjectNoteBase(MapObjectNoteBase, ABC):
    def data(self) -> List[Type[OsuNoteObjectMeta]]: pass

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
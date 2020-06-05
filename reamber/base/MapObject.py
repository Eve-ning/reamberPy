from reamber.base.mapobj.MapObjectBase import MapObjectBase
from typing import TypeVar

Base = TypeVar('Base', bound=MapObjectBase)


class MapObject:

    def addOffset(self, by: float):
        """ Move all by a specific ms """
        self.notes.addOffset(by)
        self.bpms.addOffset(by)

    # @property
    # @abstractmethod
    # def notes(self) -> Base: pass
    #
    # @property
    # @abstractmethod
    # def bpms(self) -> Base: pass

    # The TRUE nature of notes and bpms is MapObjectNotes and MapObjectBpms respectively
    # The reason for having a Union with List[NoteObject] is to facilitate the __init__ generated.
    # Having a custom __init__ would break a lot of subclasses so I just used a __post_init__ correction.
    # notes: Union[MapObjectNotes, List[NoteType]] = field(default_factory=lambda: MapObjectNotes())
    # bpms:  Union[MapObjectBpms,  List[BpmType]]   = field(default_factory=lambda: MapObjectBpms())

    # def _recast(self):
    #     self._recast()
    #     """ Recast helps recast all List[Singulars] into the correct base class """
    #     self.notes = MapObjectNotes(self.notes)
    #     self.bpms  = MapObjectBpms(self.bpms)
    #
    # def __post_init__(self) -> None:
    #     """ This corrects all List objects that can be implicitly casted as the classes """

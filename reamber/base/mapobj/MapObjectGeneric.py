from reamber.base.TimedObject import TimedObject
from abc import abstractmethod
from typing import List, Tuple


class MapObjectGeneric:
    """ A class to handle all derives' offset-related functions
    The data(self) function must be overridden for this to work.
    """

    @abstractmethod
    def data(self) -> List[TimedObject]:
        """ The factory method to grab the data from derived classes """
        raise NotImplementedError

    def sorted(self) -> List[TimedObject]:
        """ Returns a copy of Sorted objects, by offset"""
        return sorted(self.data(), key=lambda tp: tp.offset)

    def addOffset(self, by: float):
        """ Move all bpms by a specific ms """
        for obj in self: obj.offset += by

    def lastOffset(self) -> float:
        """ Get Last Note Offset """
        return max([obj.offset for obj in self.data()])

    def firstOffset(self) -> float:
        """ Get First Note Offset """
        return min([obj.offset for obj in self.data()])

    def firstLastOffset(self) -> Tuple[float, float]:
        """ Get First and Last Note Offset
        This is slightly faster than separately calling the singular functions since it sorts once only
        """
        hos = self.sorted()
        return hos[0].offset, hos[-1].offset

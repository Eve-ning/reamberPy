from __future__ import annotations
from reamber.base.TimedObject import TimedObject
from abc import abstractmethod
from typing import List, Tuple, Type

""" Convention
The idea of most functions here is to be able to chain continuously, then get the result using data() or offset()
obj.func().funcOther().data()
"""


class MapObjectGeneric:
    """ A class to handle all derives' offset-related functions
    The data(self) function must be overridden for this to work.
    """

    @abstractmethod
    def __init__(self, objList: list):
        raise NotImplementedError

    @abstractmethod
    def data(self) -> List:
        """ The factory method to grab the data from derived classes """
        raise NotImplementedError

    def sorted(self) -> MapObjectGeneric:
        """ Returns a copy of Sorted objects, by offset"""
        return MapObjectGeneric(sorted(self.data(), key=lambda tp: tp.offset))

    def between(self, lowerBound, upperBound, includeEnds=True) -> MapObjectGeneric:
        """ Returns a copy of all objects that satisfies the bounds criteria """
        return self.moreThan(lowerBound, includeEnds).lessThan(upperBound, includeEnds)

    def lessThan(self, val, includeEnd=False) -> MapObjectGeneric:
        return MapObjectGeneric([obj for obj in self.data() if obj.offset <= val]) if includeEnd else \
               MapObjectGeneric([obj for obj in self.data() if obj.offset < val])

    def moreThan(self, val, includeEnd=False) -> MapObjectGeneric:
        return MapObjectGeneric([obj for obj in self.data() if obj.offset >= val]) if includeEnd else \
               MapObjectGeneric([obj for obj in self.data() if obj.offset > val])

    def instances(self, instanceOf: Type) -> MapObjectGeneric:
        """ Gets list of objects that satisfies isinstance(obj, instanceOf) """
        return MapObjectGeneric([obj for obj in self.data() if isinstance(obj, instanceOf)])

    def offsets(self) -> List[float]:
        return [obj.offset for obj in self.data()]

    def addOffset(self, by: float) -> None:
        """ Move all bpms by a specific ms """
        for obj in self.data(): obj.offset += by

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
        obj = self.sorted().data()
        return obj[0].offset, obj[-1].offset

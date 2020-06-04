from __future__ import annotations
from dataclasses import asdict
from abc import abstractmethod, ABC
from typing import List, Tuple, Type
import pandas as pd

""" Criterion
The derived object must be:
1. A List of @dataclass
2. DataFrame-able (implied in 1.) <See df(self) on how it implicitly defines a dataclass DF
"""

""" Convention
The idea of most functions here is to be able to chain continuously, then get the result using data() or offset()
obj.func().funcOther().data()

The class must also be able to be casted into a DataFrame
"""


class MapObjectBase(ABC):
    """ A class to handle all derives' offset-related functions
    Abstract Methods can be implemented via @generateAbc in this same module.
    """

    def __init__(self, *args):
        if args: list.__init__(*args)
        else: list.__init__([])

    @abstractmethod
    def data(self) -> List:
        """ The abs method to grab the data from derived classes """
        pass

    def _upcast(self, objList: List = None):
        """ The abs method to upcast to the derived class

        The premise of upcast is that if I casted all functions to this current class, it'll end up using the absmethod
        data(self), which will return None.

        Hence the derived classes should also implement upcast
        """
        self.__init__(objList)
        return self

    def df(self) -> pd.DataFrame:
        """ The object itself mu"""
        return pd.DataFrame([asdict(obj) for obj in self.data()])

    def sorted(self) -> MapObjectBase:
        """ Returns a copy of Sorted objects, by offset"""
        return self._upcast(sorted(self.data(), key=lambda tp: tp.offset))

    def between(self, lowerBound, upperBound, includeEnds=True) -> MapObjectBase:
        """ Returns a copy of all objects that satisfies the bounds criteria """
        return self.before(lowerBound, includeEnds).after(upperBound, includeEnds)

    def after(self, offset: float, includeEnd : bool = False) -> MapObjectBase:
        return self._upcast([obj for obj in self.data() if obj.offset <= offset]) if includeEnd else \
               self._upcast([obj for obj in self.data() if obj.offset < offset])

    def before(self, offset: float, includeEnd : bool = False) -> MapObjectBase:
        return self._upcast([obj for obj in self.data() if obj.offset >= offset]) if includeEnd else \
               self._upcast([obj for obj in self.data() if obj.offset > offset])

    def attributes(self, method: str) -> List:
        """ Gets a list of the attribute associated with the generic """
        return [eval(f"obj.{method}") for obj in self.data()]

    def instances(self, instanceOf: Type) -> MapObjectBase:
        """ Gets list of objects that satisfies isinstance(obj, instanceOf) """
        return self._upcast([obj for obj in self.data() if isinstance(obj, instanceOf)])

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

#
# def generateAbc(singularType: Type = None, data=True, upcast=True):
#     """ This factory creates a decorator that sets the basic necessities for anything deriving from a mapobjBase
#     It adds __init__, data, and _upcast
#     :param singularType: This must be declared if data is true
#     :param data: Default True, generates the data
#     :param upcast: Default True, generates the upcast
#     :return: """
#
#     def wrapper(cls):
#         def _data(self) -> List[singularType]:
#             return self
#
#         def _upcast(self, objList: List = None) -> cls:
#             if objList is None: objList = []
#             return cls(objList)
#
#         if data:   setattr(cls, 'data', _data)
#         if upcast: setattr(cls, '_upcast', _upcast)
#
#         return cls
#     return wrapper

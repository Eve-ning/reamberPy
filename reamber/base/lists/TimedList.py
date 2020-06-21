from __future__ import annotations
from dataclasses import asdict
from abc import abstractmethod, ABC
from typing import List, Tuple, Type
import pandas as pd
from copy import deepcopy

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


class TimedList(ABC):
    """ A class to handle all derives' offset-related functions.

    All derived class must inherit from a list of their singular type
    """

    def __init__(self, *args):
        if args: list.__init__(*args)
        else: list.__init__([])

    @abstractmethod
    def data(self) -> List:
        """ The method to grab the data from derived classes """
        pass

    @abstractmethod
    def _upcast(self, objList: List = None):
        """ The method to upcast to the derived class

        The premise of upcast is that if I casted all functions to this current class, it'll end up using the absmethod
        data(self), which will return None.

        Hence the derived classes should also implement upcast
        """
        pass

    def df(self) -> pd.DataFrame:
        """ The object itself must be df-able """
        return pd.DataFrame([asdict(obj) for obj in self.data()])

    def deepcopy(self) -> TimedList:
        return deepcopy(self)

    def sorted(self, reverse: bool = False, inplace: bool = False) -> TimedList:
        """ Sorts the list by offset

        :param reverse: Whether to sort in reverse or not
        :param inplace: Whether to just modify this instance or return a modified copy
        :return: Returns a modified copy if not inplace
        """
        if inplace: self.__init__(sorted(self.data(), key=lambda tp: tp.offset, reverse=reverse))
        else: return self._upcast(sorted(self.data(), key=lambda tp: tp.offset, reverse=reverse))

    def between(self, lowerBound, upperBound, includeEnds=True, inplace: bool = False) -> TimedList:
        """ Trims the list between specified bounds

        :param lowerBound: The lower bound in milliseconds
        :param upperBound: The upper bound in milliseconds
        :param includeEnds: Whether to include the bound ends. \
            Use after and before if you need to only include 1 end
        :param inplace: Whether to just modify this instance or return a modified copy
        :return: Returns a modified copy if not inplace
        """
        if inplace: self.before(lowerBound, includeEnds, inplace=False)\
                        .after(upperBound, includeEnds, inplace=False)
        else: return self.before(lowerBound, includeEnds, inplace=False)\
                         .after(upperBound, includeEnds, inplace=False)

    def after(self, offset: float, includeEnd : bool = False, inplace: bool = False) -> TimedList:
        """ Trims the list after specified offset

        :param offset: The lower bound in milliseconds
        :param includeEnd: Whether to include the end
        :param inplace: Whether to just modify this instance or return a modified copy
        :return: Returns a modified copy if not inplace
        """
        if inplace: self.__init__([obj for obj in self.data() if obj.offset >= offset]) if includeEnd else \
                    self.__init__([obj for obj in self.data() if obj.offset > offset])
        else: return self._upcast([obj for obj in self.data() if obj.offset >= offset]) if includeEnd else \
                     self._upcast([obj for obj in self.data() if obj.offset > offset])

    def before(self, offset: float, includeEnd : bool = False, inplace: bool = False) -> TimedList:
        """ Trims the list before specified offset

        :param offset: The upper bound in milliseconds
        :param includeEnd: Whether to include the end
        :param inplace: Whether to just modify this instance or return a modified copy
        :return: Returns a modified copy if not inplace
        """
        if inplace: self.__init__([obj for obj in self.data() if obj.offset <= offset]) if includeEnd else \
                    self.__init__([obj for obj in self.data() if obj.offset < offset])
        else: return self._upcast([obj for obj in self.data() if obj.offset <= offset]) if includeEnd else \
                     self._upcast([obj for obj in self.data() if obj.offset < offset])

    def attribute(self, method: str) -> List:
        """ Calls each obj's method with eval. Specify method with a string.

        :param method: The method to call, the string must be **EXACT**
        :return: Returns a List of the result
        """
        expression = f"_.{method}"
        asFunc = eval('lambda _: ' + expression)

        return [asFunc(_) for _ in self.data()]
        # The above is faster for some reason
        # return [eval(f"_.{method}") for _ in self.data()]

    def instances(self, instanceOf: Type, inplace: bool = False) -> TimedList:
        """ Gets all instances that match the instanceOf type

        :param instanceOf: The type to match
        :param inplace: Whether to just modify this instance or return a modified copy
        :return: Returns a modified copy if not inplace
        """
        if inplace: self.__init__([obj for obj in self.data() if isinstance(obj, instanceOf)])
        else: return self._upcast([obj for obj in self.data() if isinstance(obj, instanceOf)])

    def offsets(self) -> List[float]:
        """ Gets all offsets of the objects """
        return [obj.offset for obj in self.data()]

    def setOffsets(self, offsets: List[float]):
        """ Sets all offsets with a List """
        for offset, obj in zip(offsets, self.data()):
            obj.offset = offset

    def addOffset(self, by: float, inplace: bool = False) -> TimedList:
        """ Adds offset to all object

        :param by: The offset to move by
        :param inplace: Whether to just modify this instance or return a modified copy
        :return: Returns a modified copy if not inplace
        """
        if inplace: d = self.data()
        else: d = self.data()[:]
        for i, obj in enumerate(d):
            obj.offset += by
            d[i] = obj
        if not inplace: return self._upcast(d)

    def multOffset(self, by: float, inplace: bool = False) -> TimedList:
        """ Adds offset to all object

        :param by: The offset to move by
        :param inplace: Whether to just modify this instance or return a modified copy
        :return: Returns a modified copy if not inplace
        """
        if inplace: d = self.data()
        else: d = self.data()[:]
        for i, obj in enumerate(d):
            obj.offset *= by
            d[i] = obj
        if not inplace: return self._upcast(d)

    def lastOffset(self) -> float:
        """ Get Last Note Offset """
        if len(self.data()) == 0: return 0.0
        return max([obj.offset for obj in self.data()])

    def firstOffset(self) -> float:
        """ Get First Note Offset """
        if len(self.data()) == 0: return float("inf")
        return min([obj.offset for obj in self.data()])

    def firstLastOffset(self) -> Tuple[float, float]:
        """ Get First and Last Note Offset
        This is slightly faster than separately calling the singular functions since it sorts once only
        """
        if len(self.data()) == 0: return 0.0, float('inf')
        obj = self.sorted().data()
        return obj[0].offset, obj[-1].offset

    def duration(self) -> float:
        """ Gets the total duration of this list """
        first, last = self.firstLastOffset()
        return last - first

    def moveStartTo(self, to: float, inplace:bool = False) -> TimedList:
        """ Moves the start of this list to a specific offset

        :param to: The offset to move it to
        :param inplace: Whether to just modify this instance or return a modified copy
        :return: Returns a modified copy if not inplace
        """
        first = self.firstOffset()
        return self.addOffset(to - first, inplace=inplace)

    def moveEndTo(self, to: float, inplace:bool = False) -> TimedList:
        """ Moves the end of this list to a specific offset

        :param to: The offset to move it to
        :param inplace: Whether to just modify this instance or return a modified copy
        :return: Returns a modified copy if not inplace
        """
        last = self.lastOffset()
        return self.addOffset(to - last, inplace=inplace)

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
#         def _upcast(self, m: List = None) -> cls:
#             if m is None: m = []
#             return cls(m)
#
#         if data:   setattr(cls, 'data', _data)
#         if upcast: setattr(cls, '_upcast', _upcast)
#
#         return cls
#     return wrapper

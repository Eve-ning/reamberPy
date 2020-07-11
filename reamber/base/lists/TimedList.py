from __future__ import annotations

from abc import abstractmethod, ABC
from copy import deepcopy
from dataclasses import asdict
from typing import List, Tuple, Type, TYPE_CHECKING, Dict

import numpy as np
import pandas as pd

if TYPE_CHECKING:
    from reamber.base.Timed import Timed


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
    def __len__(self): ...

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
        if inplace: self.__init__(sorted(self.data(), reverse=reverse))
        else: return self._upcast(sorted(self.data(), reverse=reverse))

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

        :param by: The offset to add by
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
        """ Multiplies offset to all object

        :param by: The offset to multiply by
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

    def activity(self, lastOffset: float or None = None):
        """ Calculates how long each Timed Object is active. Implicitly sorts object by offset

        For example:

        The algorithm calculates this::

            SEC 1   2   3   4   5   6   7   8   9
            BPM 100 ------> 200 --> 300 -------->

        returns [(Timed<1>, 3000), (Timed<2>, 2000), (Timed<3>, 3000)]

        :param lastOffset: Last offset, if None, uses Timed.lastOffset()
        :return: A List of Tuples in the format [(Timed, Activity In ms), ...]
        """

        if lastOffset is None: lastOffset = self.lastOffset()

        # Describes the BPM and Length of it active
        # e.g. [(120.0, 2000<ms>), (180.0, 1000<ms>), ...]
        acts: List[Tuple[Timed, float]] = []

        for obj in self.sorted(reverse=True).data():
            if obj.offset >= lastOffset:
                acts.append((obj, 0.0))  # If the BPM doesn't cover any notes it is inactive
            else:
                acts.append((obj, lastOffset - obj.offset))
                lastOffset = obj.offset
        return list(reversed(acts))

    def rollingDensity(self, window: float, stride: float = None,
                       firstOffset: float = None, lastOffset: float = None) -> Dict[int, int]:
        """ Returns the Density Dictionary

        :param window: The window to search in milliseconds.
        :param stride: The stride length of each search in milliseconds, if None, stride = window
        :param firstOffset: The first offset to start search on. If None, firstOffset will be used.
        :param lastOffset: The last offset to end search on. If None, lastOffset will be used. \
            (The search will intentionally exceed if it doesn't fit.)
        :return: Dictionary of offset as key and count as value
        """
        if stride is None:
            stride = window

        ar = np.asarray(self.offsets())

        if len(self) == 0: return {a: 0 for a in range(int(firstOffset if firstOffset else 0),
                                                       int(lastOffset if lastOffset else 0),
                                                       int(stride))}
        first, last = self.firstLastOffset()
        if firstOffset is not None: first = firstOffset
        if lastOffset is not None: last = lastOffset

        counts: Dict[int, int] = {}

        for i, j in zip(range(int(first), int(last), int(stride)),
                        range(int(first + window), int(last + window), int(stride))):
            counts[i] = np.count_nonzero((ar >= i) & (ar < j))

        return counts


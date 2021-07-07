from __future__ import annotations

from abc import abstractmethod
from copy import deepcopy
from dataclasses import asdict
from typing import Tuple, List, Dict, Any

import pandas as pd

from reamber.base.Hit import Hit
from reamber.base.Hold import Hold
from reamber.base.lists.notes.HoldList import HoldList
from reamber.base.lists.notes.NoteList import NoteList


class NotePkg:
    """ This Package holds multiple note lists """

    @abstractmethod
    def hits(self) -> List[Hit]: ...

    @abstractmethod
    def holds(self) -> List[Hold]: ...

    @abstractmethod
    def data(self) -> Dict[str, NoteList]:
        """ This grabs the data from inherited instances.
        :rtype: Dict[str, NoteList]
        :return: The inherited instances must return a dictionary of the lists. \
            It is advised to follow the names used in the convention. Such as hit for hits, note for hits and holds.
        """
        ...

    @abstractmethod
    def _upcast(self, data_dict: Dict[str, NoteList]) -> NotePkg:
        """ This just upcasts the current class so that inplace methods can work
        :param data_dict: A dictionary similar to what self.data() outputs
        :rtype: NotePkg
        """
        ...

    def deepcopy(self) -> NotePkg:
        """ Creates a deep copy of itself """
        return deepcopy(self)

    def df(self) -> Dict[str, pd.DataFrame]:
        """ Creates a dict pandas DataFrame by looping through the self.data

        :return: Returns a Dictionary of pd.DataFrames
        """
        # noinspection PyDataclass,PyTypeChecker
        return {key: pd.DataFrame([asdict(obj) for obj in data]) for key, data in self.data().items()}

    def __len__(self) -> int:
        """ Returns the number of lists. For total number of items see objCount() """
        # return sum([len(data_dict) for data_dict in self.data()])
        return len(self.data())

    def __iter__(self):
        """ Yields the Dictionary item by item """
        yield from self.data()

    def obj_count(self) -> int:
        """ Returns the total sum number of items in each list. For number of lists use len() """
        return sum([len(data) for data in self.data().values()])

    def method(self, method: str, **kwargs) -> Dict[str, Any]:
        """ Calls each list's method with eval. Specify method with a string.

        :param method: The method to call, the string must be **EXACT**
        :param kwargs: The extra parameter to use
        :return: Returns a Dict as it may not return a NotePkg init-able
        """
        expression = f"_.{method}(" + ",".join([f"{k}={v}" for k, v in kwargs.items()]) + ")"
        asFunc = eval('lambda _: ' + expression)
        return {key: asFunc(_) for key, _ in self.data().items()}

        # The above is faster for some reason
        # return {key: eval(f"_.{method}(" + ",".join([f"{k}={v}" for k, v in kwargs.items()]) + ")")
        #         for key, _ in self.data().items()}

    def add_offset(self, by, inplace: bool = False) -> NotePkg:
        """ Adds Offset to all items

        :param by: The offset to add, in milliseconds
        :param inplace: Whether to just modify this instance or return a modified copy
        :return: Returns a modified copy if not inplace
        """
        if inplace: self.method('add_offset', by=by, inplace=True)
        else: return self._upcast(self.method('add_offset', by=by, inplace=False))

    def mult_offset(self, by, inplace: bool = False) -> NotePkg:
        """ Multiplies Offset to all items

        :param by: The value to multiply by
        :param inplace: Whether to just modify this instance or return a modified copy
        :return: Returns a modified copy if not inplace
        """
        if inplace: self.method('mult_offset', by=by, inplace=True)
        else: return self._upcast(self.method('mult_offset', by=by, inplace=False))

    def in_columns(self, columns: List[int], inplace: bool = False) -> NotePkg:
        """ Filters by columns for all items

        :param columns: The columns to filter by, as a list
        :param inplace: Whether to just modify this instance or return a modified copy
        :return: Returns a modified copy if not inplace
        """
        if inplace: self.method('in_columns', columns=columns, inplace=True)
        else: return self._upcast(self.method('in_columns', columns=columns, inplace=False))

    def columns(self, flatten:bool = False) -> Dict[str, List[int]] or List[int]:
        """ Gets the columns """
        return [j for i in self.method('columns').values() for j in i] if flatten else self.method('columns')

    def max_column(self) -> int:
        """ Gets the maximum column, can be used to determine Key Count if not explicitly stated """
        return max(self.method('max_column').values())

    def offsets(self, flatten:bool = False) -> Dict[str, List[float]] or List[float]:
        """ Gets the offsets

        :param flatten: Whether to return a Dict or a flattened float list. Flattening will remove categories.
        """
        return [j for i in self.method('offsets').values() for j in i] if flatten else self.method('offsets')

    def tail_offsets(self, flatten:bool = False):
        """ Gets the tail offsets from all available Hold Lists

        :param flatten: Whether to return a Dict or a flattened float list. Flattening will remove categories.
        """
        # Statement 1 loops through data and finds any Hold List, then does a dict comp
        # Statement 2 does that and flattens it with the outer list comp
        return {k: v.tail_offsets() for k, v in self.data().items() if isinstance(v, HoldList)} if not flatten else \
            [i for j in [v.tail_offsets() for k, v in self.data().items() if isinstance(v, HoldList)] for i in j]

    def first_offset(self) -> float:
        """ Gets the first offset """
        return min(self.method('first_offset').values())

    def last_offset(self) -> float:
        """ Gets the last offset """
        return max(self.method('last_offset').values())

    def first_last_offset(self) -> Tuple[float, float]:
        """ Gets the first and last offset, slightly faster because it's only sorted once """
        if len(self.offsets()) == 0: return 0.0, float("inf")
        offsets = sorted([i for j in self.offsets().values() for i in j])  # Flattens the offset list
        return offsets[0], offsets[-1]

    def describe_notes(self, rounding: int = 2):
        """ Describes a single NotePkg

        Prints out Count, Median, 75% quantile and max for each note type

        :param rounding: The decimal rounding
        """
        for s, lis in self.data().items():
            print(s)
            lis.describe_notes(rounding=rounding)

    def rolling_density(self, window: int = 1000, stride: int = None,
                        first_offset: float = None, last_offset: float = None) -> Dict[str, Dict[int, int]]:
        """ Returns the Density List Dictionary

        First offset and last offset is recalculated here in Package to make sure that the indexes are consistent.

        :param window: The window to search in milliseconds.
        :param stride: The stride length of each search in milliseconds, if None, stride = window
        :param first_offset: The first offset to start search on. If None, first_offset will be used.
        :param last_offset: The last offset to end search on. If None, last_offset will be used. \
            (The search will intentionally exceed if it doesn't fit.)
        :return: Dictionary of offset as key and count as value
        """
        return self.method('rolling_density', window=window, stride=stride,
                           first_offset=first_offset if first_offset else self.first_offset(),
                           last_offset=last_offset if last_offset else self.last_offset())

    def duration(self):
        """ Gets the duration of this package. """
        return self.last_offset() - self.first_offset()

from __future__ import annotations

from copy import deepcopy
from typing import List, Tuple, Dict, Union, overload, Any, Generator, Generic, TypeVar

import numpy as np
import pandas as pd
from pandas.core.indexing import _iLocIndexer, _LocIndexer

from reamber.base.Series import Series
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

Item = TypeVar('Item')

class TimedList(Generic[Item]):
    """ A class to handle all derives' offset-related functions.

    All derived class must inherit from a list of their singular type
    """

    # ---------- REQUIRED FOR SUBCLASSING ---------- #

    @property
    def _init_empty(self) -> dict:
        """ Initializes the DataFrame if no objects are passed to init. """
        return dict(offset=pd.Series([], dtype='float'))

    @property
    def _item_class(self) -> type:
        """ This is the class type for a singular item, this is needed for correct casting when indexing. """
        return Timed

    # This is required so that the typing returns are correct.
    @overload
    def __getitem__(self, item: slice) -> TimedList: ...
    @overload
    def __getitem__(self, item: list) -> TimedList: ...
    @overload
    def __getitem__(self, item: Any) -> TimedList: ...
    @overload
    def __getitem__(self, item: int) -> Timed: ...
    def __getitem__(self, item):
        # This is an interesting way to use the callee class
        # e.g., if the subclass, Note, calls this, it'll be Note(self.df[item]).
        # self(self.df[item]) doesn't work as self is an instance.

        if isinstance(item, int):
            return self._item_class(**self.df.iloc[item].to_dict())
        else:
            return self.__class__(self.df[item])

    # ---------- REQUIRED FOR SUBCLASSING ---------- #

    _df: pd.DataFrame

    def __init__(self, objs: Union[List[Item], Item, pd.DataFrame]):
        """ Creates the List from a List of Timed object or from a DataFrame.

        DF(DF()) -> DF works as expected but we make it clearer
        """
        if isinstance(objs, TimedList):
            # If it's another Timed List, we just copy over
            self.df = objs.df
        elif isinstance(objs, pd.DataFrame):
            self.df = objs
        elif isinstance(objs, Timed):
            # If it's a single Timed, we make it a list
            self.df = self._join([objs])
        elif isinstance(objs, List):
            if len(objs) == 0:
                # Because empty lists cannot provide columns, we MUST have a initial DF.
                self.df = pd.DataFrame(self._init_empty)
            else:
                assert all([isinstance(obj, Timed) for obj in objs]),\
                    f"All objects must be Timed. Found incorrectly typed objects: " \
                    f"{[type(s) for s in objs if not isinstance(s, Timed)][:5]}"
                self.df = self._join(objs)

    def __len__(self) -> int:
        return len(self.df)

    def __iter__(self) -> Generator[Item]:
        for i in self.df.iterrows():
            # noinspection PyUnresolvedReferences
            yield self._item_class.from_series(i[-1])

    def __eq__(self, other: TimedList): return self.df == other.df
    def __gt__(self, other: TimedList): return self.df > other.df
    def __ge__(self, other: TimedList): return self.df >= other.df
    def __lt__(self, other: TimedList): return self.df < other.df
    def __le__(self, other: TimedList): return self.df <= other.df
    def __repr__(self):
        return self.df.__repr__()

    def append(self, val: Union[Series, TimedList, pd.Series, pd.DataFrame],
               ignore_index=True, verify_integrity=False, sort=False):
        if isinstance(val, Series): val = val.data
        if isinstance(val, TimedList): val = val.df
        return self.__class__(
            self.df.append(val, ignore_index=ignore_index, verify_integrity=verify_integrity, sort=sort)
        )

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    @df.setter
    def df(self, value):
        self._df = value

    def to_numpy(self) -> np.ndarray:
        return self.df.to_numpy()

    @staticmethod
    def _join(objs: List[Timed]) -> pd.DataFrame:
        return pd.DataFrame([o.data for o in objs])

    @property
    def offsets(self) -> Union[pd.Series, Any]:
        # The return type is Any to prevent Type Checking during comparison
        return self.df['offset']

    @offsets.setter
    def offsets(self, values):
        self.df['offset'] = values

    def __setitem__(self, key, value):
        self.df.iloc.__setitem__(key, value)

    def deepcopy(self):
        return deepcopy(self)

    def describe(self) -> pd.DataFrame:
        return self.df.describe()

    def sorted(self, reverse: bool = False):
        """ Sorts the list by offset

        :param reverse: Whether to sort in reverse or not
        :return: Returns a modified copy if not inplace
        """

        return self.__class__(self.df.sort_values('offset', ascending=not reverse))

    def between(self,
                lower_bound: float,
                upper_bound: float,
                include_ends: Tuple[bool, bool] = (True, False)) -> TimedList:
        """ Trims the list between specified bounds

        :param lower_bound: The lower bound in milliseconds
        :param upper_bound: The upper bound in milliseconds
        :param include_ends: Whether to include the bound ends.
            The first argument is for before, second is for after
        :return: Returns a modified copy if not inplace
        """
        include_ends = (include_ends, include_ends) if isinstance(include_ends, bool) else include_ends
        return self.after(lower_bound, include_ends[0]).before(upper_bound, include_ends[1])

    def after(self,
              offset: float,
              include_end : bool = False):
        """ Trims the list to after specified offset

        :param offset: The lower bound in milliseconds
        :param include_end: Whether to include the end
        :return: Returns a modified copy if not inplace
        """
        # noinspection PyTypeChecker
        return self[self.offsets >= offset] if include_end else self[self.offsets > offset]

    def before(self, offset: float,
               include_end : bool = False):
        """ Trims the list to before specified offset

        :param offset: The upper bound in milliseconds
        :param include_end: Whether to include the end
        :return: Returns a modified copy if not inplace
        """
        # noinspection PyTypeChecker
        return self[self.offsets <= offset] if include_end else self[self.offsets < offset]

    def attribute(self, method: str) -> List:
        """ Calls each obj's method with eval. Specify method with a string.

        :param method: The method to call, the string must be **EXACT**
        :return: Returns a List of the result
        """
        raise DeprecationWarning()
        expression = f"_.{method}"
        asFunc = eval('lambda _: ' + expression)

        return [asFunc(_) for _ in self.data()]
        # The above is faster for some reason
        # return [eval(f"_.{method}") for _ in self.data()]

    def last_offset(self) -> float:
        """ Get Last Note Offset """
        if len(self.df) == 0: return 0.0
        return max(self.offsets)

    def first_offset(self) -> float:
        """ Get First Note Offset """
        if len(self.df) == 0: return float("inf")
        return min(self.offsets)

    def first_last_offset(self) -> Tuple[float, float]:
        """ Get First and Last Note Offset """
        if len(self.df) == 0: return 0.0, float('inf')
        offsets = self.offsets
        return min(offsets), max(offsets)

    def move_start_to(self, to: float) -> TimedList:
        """ Moves the start of this list to a specific offset. This creates a copy.

        :param to: The offset to move it to
        :return: Returns a modified copy if not inplace
        """
        first = self.first_offset()
        this = self.deepcopy()
        this.offsets += to - first
        return this

    def move_end_to(self, to: float) -> TimedList:
        """ Moves the end of this list to a specific offset

        :param to: The offset to move it to
        :return: Returns a modified copy if not inplace
        """
        last = self.last_offset()
        this = self.deepcopy()
        this.offsets += to - last
        return this

    def activity(self, last_offset: float or None = None) -> np.ndarray:
        """ Calculates how long each Timed Object is active.

        For example:

        The algorithm calculates this::

            SEC 1   2   3   4   5   6   7   8   9
            BPM 100 ------> 200 --> 300 -------->

        :param last_offset: Last offset, if None, uses Timed.last_offset()
        :return: np.ndarray of the activity/offset differences.
        """

        return np.diff(self.sorted().offsets, append=last_offset if last_offset else self.last_offset())

    def rolling_density(self,
                        window: float,
                        stride: float = None,
                        first_offset: float = None,
                        last_offset: float = None) -> Dict[int, int]:
        """ Returns the Density Dictionary

        :param window: The window to search in milliseconds.
        :param stride: The stride length of each search in milliseconds, if None, stride = window
        :param first_offset: The first offset to start search on. If None, first_offset will be used.
        :param last_offset: The last offset to end search on. If None, last_offset will be used. \
            (The search will intentionally exceed if it doesn't fit.)
        :return: Dictionary of offset as key and count as value
        """
        if stride is None:
            stride = window

        ar = self.offsets.to_numpy()

        if len(self) == 0: return {a: 0 for a in range(int(first_offset if first_offset else 0),
                                                       int(last_offset if last_offset else 0),
                                                       int(stride))}
        first, last = self.first_last_offset()
        if first_offset is not None: first = first_offset
        if last_offset is not None: last = last_offset

        counts: Dict[int, int] = {}

        for i, j in zip(range(int(first), int(last), int(stride)),
                        range(int(first + window), int(last + window), int(stride))):
            counts[i] = np.count_nonzero((ar >= i) & (ar < j))

        return counts

    @property
    def iloc(self) -> _iLocIndexer:
        """ Note that this is simply a shorthard for self.df.iloc.

        Thus indexing from this will yield a DataFrame. """
        return self.df.iloc

    @property
    def loc(self) -> _LocIndexer:
        """ Note that this is simply a shorthard for self.df.loc.

        Thus indexing from this will yield a DataFrame. """
        return self.df.loc

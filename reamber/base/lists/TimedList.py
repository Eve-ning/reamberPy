from __future__ import annotations

from copy import deepcopy
from typing import List, Tuple, Dict, overload, Any, Generator, Generic, TypeVar

import numpy as np
import pandas as pd
# noinspection PyProtectedMember
from pandas.core.indexing import _iLocIndexer, _LocIndexer

from reamber.base.Property import list_props
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


@list_props(Timed)
class TimedList(Generic[Item]):
    """ A class to handle all derives' offset-related functions.

    All derived class must inherit from a list of their singular type
    """

    _df: pd.DataFrame

    # ---------- REQUIRED FOR SUBCLASSING ---------- #

    @staticmethod
    def _default() -> dict:
        """ Returns a dict for the default values. """
        return dict(offset=pd.Series(0, dtype='float'))

    @property
    def _item_class(self) -> type:
        """ This is the class type for a singular item, this is needed for correct casting when indexing. """
        return Item

    # This is required so that the typing returns are correct.
    @overload
    def __getitem__(self, item: slice) -> TimedList:
        ...

    @overload
    def __getitem__(self, item: list) -> TimedList:
        ...

    @overload
    def __getitem__(self, item: Any) -> TimedList:
        ...

    @overload
    def __getitem__(self, item: int) -> Item:
        ...

    def __getitem__(self, item):
        """ Implements indexing

        Examples:
            You can index any ``TimedList`` subclass with these

            >>> tl = TimedList([Timed(offset=1000),
            ...                 Timed(offset=2000),
            ...                 Timed(offset=3000)])
            >>> tl.offset.tolist()
            [1000, 2000, 3000]

            Slice Indexing

            >>> tl[0:2].offset.tolist()
            [1000, 2000]

            Int Indexing

            >>> tl[0].offset
            1000

        Returns:
            A ``TimedList`` if it's a non-int, else ``Timed`` object.

        """
        if isinstance(item, int):
            return self._item_class()(**self.df.iloc[item].to_dict())
        else:
            return self.__class__(self.df[item])

    def __iter__(self) -> Generator[Item]:
        """ Provides an interface to ``pd.iterrows``.

        Examples:
            >>> tl = TimedList([Timed(offset=1000),
            ...                 Timed(offset=2000),
            ...                 Timed(offset=3000)])
            >>> for t in tl:
            ...     type(t)
            <class 'reamber.base.Timed.Timed'>
            <class 'reamber.base.Timed.Timed'>
            <class 'reamber.base.Timed.Timed'>

            If this was ran under ``HitList`` it would output
            ``Hit`` as the class.

        Notes:
            This will re-cast each object to the ``item_class``

        Returns:
            A ``Generator[Item]``

        """
        for i in self.df.iterrows():
            # noinspection PyUnresolvedReferences
            yield self._item_class().from_series(i[-1])

    # ---------- REQUIRED FOR SUBCLASSING ---------- #
    @overload
    def __init__(self, objs: List[Item]):
        ...

    @overload
    def __init__(self, objs: Item):
        ...

    @overload
    def __init__(self, objs: pd.DataFrame):
        ...

    def __init__(self, objs: List[Item] | Item | pd.DataFrame):
        """ Creates ``TimedList`` from ``List[Timed]`` or a ``pd.DataFrame``.

        Examples:
            >>> tl = TimedList([Timed(offset=1000),
            ...                 Timed(offset=2000),
            ...                 Timed(offset=3000)])

            From another ``TimedList``

            >>> tl2 = TimedList(tl)
            >>> tl2.offset.tolist()
            [1000, 2000, 3000]

            From a ``pd.DataFrame``

            >>> tl2 = TimedList(tl.df)
            >>> tl2.offset.tolist()
            [1000, 2000, 3000]

            From a single ``Timed`` object

            >>> tl2 = TimedList(Timed(offset=1000))
            >>> tl2.offset.tolist()
            [1000]

            From a empty ``List``

            >>> tl2 = TimedList([])
            >>> tl2.offset.tolist()
            []

            From a ``List[Timed]``

            >>> tl2 = TimedList([Timed(offset=1000),
            ...                  Timed(offset=2000)])
            >>> tl2.offset.tolist()
            [1000, 2000]

            It will reject if object isn't a subclass of ``Timed``

            >>> tl2 = TimedList([200, 300]) # doctest: +ELLIPSIS
            Traceback (most recent call last):
                ...
            AssertionError: All objects must be Timed. Found incorrectly typed objects: [<class 'int'>, <class 'int'>]
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
                # Because empty lists cannot provide columns, we MUST have a initial DF, we create one with the
                # default and empty it.
                self.df = pd.DataFrame(self._default())[:0]
            else:
                if all([isinstance(obj, Timed) for obj in objs]):
                    self.df = self._join(objs)
                else:
                    raise AssertionError(f"All objects must be Timed. Found incorrectly typed objects: "
                                         f"{[type(s) for s in objs if not isinstance(s, Timed)][:5]}")

    @classmethod
    def empty(cls, rows: int) -> TimedList:
        """ Creates an empty class of rows

        Args:
            rows: Number of objects

        Returns:
            ``TimedList`` with ``rows`` default
        """
        df = pd.DataFrame(cls._default())
        return cls(df.loc[df.index.repeat(rows)].reset_index())

    def __len__(self) -> int:
        return len(self.df)

    def __eq__(self, other: TimedList):
        return self.df == other.df

    def __gt__(self, other: TimedList):
        return self.df > other.df

    def __ge__(self, other: TimedList):
        return self.df >= other.df

    def __lt__(self, other: TimedList):
        return self.df < other.df

    def __le__(self, other: TimedList):
        return self.df <= other.df

    def __repr__(self):
        return self.df.__repr__()

    def append(self,
               val: Series | TimedList | pd.Series | pd.DataFrame,
               sort: bool = False) -> TimedList:
        """ Appends to the end of List

        Examples:

            >>> tl = TimedList([Timed(offset=1000),
            ...                 Timed(offset=2000)])
            >>> tl.offset.tolist()
            [1000, 2000]

            >>> tl.append(
            ...     Timed(offset=1500)
            ... ).offset.tolist()
            [1000, 2000, 1500]

            >>> tl.append(
            ...     Timed(offset=1500), sort=True
            ... ).offset.tolist()
            [1000, 1500, 2000]

            # >>> tl.append(
            # ...     Timed(offset=1500).data, sort=True
            # ... ).offset.tolist()
            # [1000, 1500, 2000]

        Args:
            val: Object to append
            sort: Whether to sort it after append

        Returns:
            The appended ``TimedList``.

        """
        if isinstance(val, Series): val = val.data.to_frame().T
        if isinstance(val, TimedList): val = val.df
        obj = self.__class__(pd.concat([self.df, val], ignore_index=True))
        return obj.sorted() if sort else obj

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    # noinspection PyUnresolvedReferences
    @df.setter
    def df(self, value):
        self._df = value

    def to_numpy(self) -> np.ndarray:
        return self.df.to_numpy()

    @staticmethod
    def _join(objs: List[Timed]) -> pd.DataFrame:
        return pd.DataFrame([o.data for o in objs])

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
              include_end: bool = False):
        """ Trims the list to after specified offset

        :param offset: The lower bound in milliseconds
        :param include_end: Whether to include the end
        :return: Returns a modified copy if not inplace
        """
        # noinspection PyTypeChecker
        return self[self.offset >= offset] if include_end else self[self.offset > offset]

    def before(self, offset: float,
               include_end: bool = False):
        """ Trims the list to before specified offset

        :param offset: The upper bound in milliseconds
        :param include_end: Whether to include the end
        :return: Returns a modified copy if not inplace
        """
        # noinspection PyTypeChecker
        return self[self.offset <= offset] if include_end else self[self.offset < offset]

    def last_offset(self):
        """ Get Last Note Offset """
        if len(self.df) == 0: return None
        return max(self.offset)

    def first_offset(self):
        """ Get First Note Offset """
        if len(self.df) == 0: return None
        return min(self.offset)

    def first_last_offset(self):
        """ Get First and Last Note Offset """
        if len(self.df) == 0: return None, None
        offsets = self.offset
        return min(offsets), max(offsets)

    def move_start_to(self, to: float) -> TimedList:
        """ Moves the start of this list to a specific offset. This creates a copy.

        :param to: The offset to move it to
        :return: Returns a modified copy if not inplace
        """
        first = self.first_offset()
        this = self.deepcopy()
        this.offset += to - first
        return this

    def move_end_to(self, to: float) -> TimedList:
        """ Moves the end of this list to a specific offset

        :param to: The offset to move it to
        :return: Returns a modified copy if not inplace
        """
        last = self.last_offset()
        this = self.deepcopy()
        this.offset += to - last
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

        return np.diff(self.sorted().offset, append=last_offset if last_offset else self.last_offset())

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

        ar = self.offset.to_numpy()

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

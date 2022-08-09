from __future__ import annotations

from typing import List, Tuple, Dict, Union, overload, Generator, Generic, \
    TypeVar

import numpy as np
import pandas as pd
# noinspection PyProtectedMember
from pandas.core.indexing import _iLocIndexer, _LocIndexer

from reamber.base.Property import Properties
from reamber.base.Series import Series
from reamber.base.Timed import Timed

"""Criterion
The derived object must be:
1. A List of @dataclass
2. DataFrame-able (implied in 1.) <See df(self) on how it implicitly defines a dataclass DF
"""

Item = TypeVar('Item', bound=Timed)


class TimedList(Generic[Item]):
    """A class to handle all derives' offset-related functions.

    All derived class must inherit from a list of their singular type
    """

    _df: pd.DataFrame

    @property
    def offset(self) -> pd.Series: ...

    @offset.setter
    def offset(self, val): ...

    @staticmethod
    def _default() -> dict: ...

    @staticmethod
    def _item_class() -> type: ...

    @staticmethod
    def props() -> Properties: ...

    # This is required so that the typing returns are correct.
    @overload
    def __getitem__(self, item: slice) -> TimedList: ...

    @overload
    def __getitem__(self, item: int) -> Item: ...

    def __setitem__(self, key, value) -> None: ...

    def __iter__(self) -> Generator[Item]: ...

    def __init__(self, objs: Union[List[Item], Item, pd.DataFrame]): ...

    @classmethod
    def empty(cls, rows: int) -> TimedList: ...

    def __len__(self) -> int: ...

    def __eq__(self, other: TimedList): ...

    def __gt__(self, other: TimedList): ...

    def __ge__(self, other: TimedList): ...

    def __lt__(self, other: TimedList): ...

    def __le__(self, other: TimedList): ...

    def __repr__(self): ...

    def append(self, val: Union[Series, TimedList, pd.Series, pd.DataFrame],
               sort=False) -> TimedList: ...

    @staticmethod
    def from_dict(d: List[Dict] | Dict[str, List]) -> TimedList: ...

    @property
    def df(self) -> pd.DataFrame: ...

    @df.setter
    def df(self, value) -> None: ...

    def to_numpy(self) -> np.ndarray: ...

    @staticmethod
    def _join(objs: List[Timed]) -> pd.DataFrame: ...

    def deepcopy(self) -> TimedList: ...

    def describe(self) -> pd.DataFrame: ...

    def sorted(self, reverse: bool = False) -> TimedList: ...

    def between(self,
                lower_bound: float,
                upper_bound: float,
                include_ends: Tuple[bool, bool] = (
                True, False)) -> TimedList: ...

    def after(self,
              offset: float,
              include_end: bool = False) -> TimedList: ...

    def before(self, offset: float,
               include_end: bool = False) -> TimedList: ...

    def attribute(self, method: str) -> List: ...

    def last_offset(self) -> float: ...

    def first_offset(self) -> float: ...

    def first_last_offset(self) -> Tuple[float, float]: ...

    def move_start_to(self, to: float) -> TimedList: ...

    def move_end_to(self, to: float) -> TimedList: ...

    def time_diff(self, last_offset: float or None = None) -> np.ndarray: ...

    @property
    def iloc(self) -> _iLocIndexer: ...

    @property
    def loc(self) -> _LocIndexer: ...

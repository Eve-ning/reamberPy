from __future__ import annotations

from copy import deepcopy
from functools import total_ordering

import numpy as np
import pandas as pd

from reamber.base import item_props
from reamber.base.Series import Series


class Timed(Series):

    _props = dict(offset='float')

    def __init__(self, offset: float, **kwargs): ...
    @property
    def offset(self) -> float: ...
    @offset.setter
    def offset(self, val) -> None: ...
    def __eq__(self, other: Timed): ...
    def __gt__(self, other: Timed): ...
    def deepcopy(self) -> Timed: ...
    def _from_series_allowed_names() -> list: ...



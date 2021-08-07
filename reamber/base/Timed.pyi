from __future__ import annotations

import numpy as np
import pandas as pd

from reamber.base.Property import Properties
from reamber.base.Series import Series


class Timed(Series):

    _props = dict(offset=['float', 0.0])

    def __init__(self, offset: float, **kwargs): ...
    @property
    def offset(self) -> float: ...
    @offset.setter
    def offset(self, val) -> None: ...
    def __eq__(self, other: Timed): ...
    def __gt__(self, other: Timed): ...
    def deepcopy(self) -> Timed: ...
    @classmethod
    def props(cls) -> Properties: ...


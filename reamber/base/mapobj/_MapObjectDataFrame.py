import pandas as pd
from abc import abstractmethod
from reamber.base.TimedObject import TimedObject
from dataclasses import asdict
from typing import List

""" Deprecated
This has been moved to MapObjectBase
"""


class _MapObjectDataFrame:
    """ The purpose of this whole class is to declare that a class can be coerced into a Pandas DataFrame.
    I kept this separate from Generic since it deals with base python classes."""

    def __init__(self):
        raise DeprecationWarning

    @abstractmethod
    def data(self) -> List[TimedObject]:
        raise NotImplementedError

    def df(self) -> pd.DataFrame:
        return pd.DataFrame([asdict(obj) for obj in self.data()])

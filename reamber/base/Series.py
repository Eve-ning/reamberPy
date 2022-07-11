from __future__ import annotations

from copy import deepcopy

import numpy as np
import pandas as pd


class Series:
    data: pd.Series

    def __init__(self, **kwargs):
        """If init from same class, we use kwarg to bypass the init"""
        self.data = pd.Series(data=kwargs)

    def __repr__(self):
        return self.data.__repr__()

    @staticmethod
    def _from_series_allowed_names():
        """Args not in list will be excluded in from_series"""
        return []

    @classmethod
    def from_series(cls, data: pd.Series):
        """An alternative __init__: Uses Series' to_dict as __init__ arguments

        Notes:
            Works by checking if data has column names in __init__ signature
            _from_series_allowed_names.
        """
        try:
            return cls(
                **{k: v for k, v in data.to_dict().items() if k in
                   cls._from_series_allowed_names()}
            )
        except TypeError as e:
            raise TypeError(
                f"from_series call is missing arguments: {e.args}. "
                f"Make sure that those columns exist."
            )

    def __eq__(self, other: Series):
        return np.all(self.data == other.data)

    def deepcopy(self):
        """Returns a deep copy of itself"""
        return deepcopy(self)

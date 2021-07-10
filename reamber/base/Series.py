import pandas as pd


class Series:
    data: pd.Series

    def __init__(self, **kwargs):
        """ If initializing from the same class, we can use the data kwarg to bypass the init """

        self.data = pd.Series(data=kwargs)

    def __repr__(self):
        return self.data.__repr__()

    @staticmethod
    def _from_series_allowed_names():
        """ Allowed names is to aid from_series from detecting what excess columns to exclude. """
        return []

    @classmethod
    def from_series(cls, data: pd.Series):
        """ This is an alternative to __init__, it takes the Series' to_dict as the arguments for __init__.

        So as long as the Series contains the correct column names as the __init__ signature, it will work.

        This uses the _allowed_names from the cls, so if you want to restrict what arguments are allowed, override that.
        """
        try:
            return cls(**{k: v for k, v in data.to_dict().items() if k in cls._from_series_allowed_names()})
        except TypeError as e:
            raise TypeError(f"from_series call is missing arguments: {e.args}. Make sure that those columns exist.")

import pandas as pd

from reamber.base.Timed import Timed


class SvObj(Timed):
    """ This isn't a base object since it's not a required object for any map.

        This is just to facilitate SvSequence and SvPkg

        Offset uses milliseconds units. Negative values are allowed

        A Fixed Sv means recalculation will avoid changing the value unless explicitly stated.
        """

    _props = dict(multiplier=['float', 1.0], fixed=['bool', False])

    def __init__(self, offset: float, multiplier: float = 1.0, **kwargs): ...

    @property
    def multiplier(self) -> pd.Series: ...
    @multiplier.setter
    def multiplier(self, val) -> None: ...
    @property
    def fixed(self) -> pd.Series: ...
    @fixed.setter
    def fixed(self, val) -> None: ...

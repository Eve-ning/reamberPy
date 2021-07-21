from typing import Dict, Any

import pandas as pd

from reamber.base.Timed import Timed


class QuaSv(Timed):

    def __init__(self, offset: float, multiplier: float = 1.0, **kwargs): ...

    def to_yaml_dict(self) -> Dict[str, Any]: ...
    @staticmethod
    def from_yaml_dict(d: Dict[str, Any]): ...
    @property
    def multiplier(self) -> pd.Series: ...
    @multiplier.setter
    def multiplier(self, val) -> None: ...

from dataclasses import dataclass
from reamber.base.Timed import Timed


@dataclass
class SvObj(Timed):
    """ This isn't a base object since it's not a required object for any map.

    This is just to facilitate SvSequence and SvPkg

    Offset uses milliseconds units. Negative values are allowed

    A Fixed Sv means recalculation will avoid changing the value unless explicitly stated.
    """

    multiplier: float = 1.0
    fixed: bool = False

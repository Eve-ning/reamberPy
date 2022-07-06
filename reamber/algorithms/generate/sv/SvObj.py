from dataclasses import dataclass

from reamber.base import item_props
from reamber.base.Timed import Timed


@item_props()
class SvObj(Timed):
    """ This isn't a base object since it's not a required object for any map.

        This is just to facilitate SvSequence and SvPkg

        Offset uses milliseconds units. Negative values are allowed

        A Fixed Sv means recalculation will avoid changing the value unless explicitly stated.
        """

    _props = dict(multiplier=['float', 1.0],
                  fixed=['bool', False])

    def __init__(self,
                 offset: float,
                 multiplier: float = 1.0,
                 **kwargs):
        # raise DeprecationWarning("SV Sequencing is not available in this version. It'll be restored soon.")
        super().__init__(
            offset=offset, multiplier=multiplier, **kwargs
        )


from __future__ import annotations

from functools import total_ordering

from reamber.base.Property import item_props, Properties
from reamber.base.Series import Series


@total_ordering
@item_props()
class Timed(Series):
    """This is the base class where all timed objects must stem from. """

    _props = dict(offset=['float', 0.0])

    def __init__(self, offset: float, **kwargs):
        """Initializer

        Examples:
            >>> t = Timed(offset=1000)
            >>> t.offset
            1000

        Args:
            offset: Offset in ms
        """
        super().__init__(offset=offset, **kwargs)

    def __gt__(self, other: Timed):
        return self.offset > other.offset

    @classmethod
    def props(cls):
        return Properties(cls._props)

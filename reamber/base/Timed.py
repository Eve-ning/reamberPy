from __future__ import annotations

from copy import deepcopy
from functools import total_ordering

import numpy as np

from reamber.base.Property import item_props, Properties
from reamber.base.Series import Series


@total_ordering
@item_props()
class Timed(Series):
    """ This is the base class where all timed objects must stem from. """

    _props = dict(offset=['float', 0.0])

    def __init__(self, offset: float, **kwargs):
        """ Initializer

        Examples:
            >>> t = Timed(offset=1000)
            >>> t.offset
            1000

        Args:
            offset: Offset in ms
        """
        super().__init__(offset=offset, **kwargs)

    def __eq__(self, other: Timed):
        return np.all(self.data == other.data)

    def __gt__(self, other: Timed):
        return self.offset > other.offset

    def deepcopy(self):
        """ Returns a deep copy of itself """
        return deepcopy(self)

    @classmethod
    def props(cls):
        return Properties(cls._props)

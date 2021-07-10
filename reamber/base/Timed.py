from __future__ import annotations

from copy import deepcopy
from functools import total_ordering

import numpy as np

from reamber.base.Series import Series


@total_ordering
class Timed(Series):
    """ This is the base class where all timed objects must stem from. """

    def __init__(self, offset: float, **kwargs):
        super(Timed, self).__init__(offset=offset, **kwargs)

    @property
    def offset(self):
        return self.data['offset']

    @offset.setter
    def offset(self, val):
        self.data['offset'] = val

    def __eq__(self, other: Timed):
        return np.all(self.data == other.data)

    def __gt__(self, other: Timed):
        return self.offset > other.offset

    def deepcopy(self):
        """ Returns a deep copy of itself """
        return deepcopy(self)

    @staticmethod
    def _from_series_allowed_names():
        return [*Series._from_series_allowed_names(), 'offset']



from __future__ import annotations
from dataclasses import dataclass, asdict
from functools import total_ordering
from copy import deepcopy

@total_ordering
@dataclass
class Timed:
    """ This is the base class where all timed objects must stem from. """

    offset: float = 0.0

    def __eq__(self, other: Timed):
        return asdict(self) == asdict(other)

    def __gt__(self, other: Timed):
        return self.offset > other.offset

    def deepcopy(self):
        """ Returns a deep copy of itself """
        return deepcopy(self)

    def addOffset(self, by: float, inplace: bool = False):
        this = self if inplace else self.deepcopy()
        this.offset += by
        return None if inplace else this

    def multOffset(self, by: float, inplace: bool = False):
        this = self if inplace else self.deepcopy()
        this.offset *= by
        return None if inplace else this



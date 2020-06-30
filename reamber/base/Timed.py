from __future__ import annotations
from dataclasses import dataclass, asdict
from functools import total_ordering

@total_ordering
@dataclass
class Timed:
    """ This is the base class where all timed objects must stem from. """

    offset: float = 0.0

    def __eq__(self, other: Timed):
        return asdict(self) == asdict(other)

    def __gt__(self, other: Timed):
        return self.offset > other.offset

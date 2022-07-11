from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from reamber.algorithms.playField import PlayField

class PFDrawable(ABC):
    """All PlayField Drawing classes inherit from enables the __add__ op"""
    @abstractmethod
    def draw(self, pf: 'PlayField') -> 'PlayField': ...

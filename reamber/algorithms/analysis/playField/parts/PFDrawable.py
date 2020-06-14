from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from reamber.algorithms.analysis.playField.PlayField import PlayField


class PFDrawable(ABC):
    """ All PlayField Drawing classes must inherit from this to enable the __add__ op """
    @abstractmethod
    def draw(self, pf: 'PlayField') -> 'PlayField': ...

from abc import ABC, abstractmethod


class PFDrawable(ABC):
    """ All PlayField Drawing classes must inherit from this to enable the __add__ op """
    @abstractmethod
    def draw(self, pf: 'PlayField') -> 'PlayField': ...

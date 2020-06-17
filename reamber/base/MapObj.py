from reamber.base.lists.NotePkg import NotePkg
from reamber.base.lists.BpmList import BpmList
from abc import ABC, abstractmethod
from typing import Dict
from reamber.base.lists.TimedList import TimedList


class MapObj(ABC):
    """ This class should be inherited by all Map Objects

    They must inherit the data method, which extracts all data they hold.
    They are also assumed to be a TimedList.
    """

    notes: NotePkg
    bpms: BpmList

    @abstractmethod
    def data(self) -> Dict[str, TimedList]:
        """ Gets the data as a dictionary """
        ...

    def addOffset(self, by: float):
        """ Move all by a specific ms """

        for k, i in self.data().items():
            i.addOffset(by)
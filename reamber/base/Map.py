from reamber.base.lists.NotePkg import NotePkg
from reamber.base.lists.BpmList import BpmList
from abc import ABC, abstractmethod
from typing import Dict, TYPE_CHECKING, Tuple, List
from reamber.base.lists.TimedList import TimedList

if TYPE_CHECKING:
    from reamber.base.Bpm import Bpm


class Map(ABC):
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

    def activity(self, lastOffset: float or None = None) -> List[Tuple[Bpm, float]]:
        """ Calculates how long the Bpm is active. Implicitly sorts BPM

        For example

        The algorithm calculates this::

            SEC 1   2   3   4   5   6   7   8   9
            BPM 100 ------> 200 --> 300 -------->

        returns [(BPMPoint<100>, 3000), (BPMPoint<200>, 2000), (BPMPoint<300>, 3000)]

        :param lastOffset: If not None, then this offset will be used to terminate activity, else last note offset will\
            be used.
        :return: A List of Tuples in the format [(BPMPoint, Activity In ms), ...]
        """
        return self.bpms.activity(lastOffset) if lastOffset else self.bpms.activity(self.notes.lastOffset())

    def aveBpm(self) -> float:
        activitySum = 0
        sumProd = 0
        for bpm, activity in self.activity():
            activitySum += activity
            sumProd += bpm.bpm * activity
        return sumProd / activitySum


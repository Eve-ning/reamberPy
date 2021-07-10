from __future__ import annotations

import datetime
from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Dict, TYPE_CHECKING, Tuple, List

from reamber.base.lists.BpmList import BpmList
from reamber.base.lists.NotePkg import NotePkg
from reamber.base.lists.TimedList import TimedList

if TYPE_CHECKING:
    from reamber.base import Bpm


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

    def deepcopy(self):
        """ Returns a deep copy of itself """
        return deepcopy(self)

    def add_offset(self, by: float, inplace: bool = False):
        """ Move all by a specific ms """
        this = self if inplace else self.deepcopy()
        for k, i in this.data().items():
            i.offsets += by
        return None if inplace else this

    def mult_offset(self, by: float, inplace: bool = False):
        """ Multiply all by a value """
        this = self if inplace else self.deepcopy()
        for k, i in this.data().items():
            i.offsets *= by
        return None if inplace else this

    def activity(self, last_offset: float or None = None) -> List[Tuple['Bpm', float]]:
        """ Calculates how long the Bpm is active. Implicitly sorts BPM

        For example

        The algorithm calculates this::

            SEC 1   2   3   4   5   6   7   8   9
            BPM 100 ------> 200 --> 300 -------->

        returns [(BPMPoint<100>, 3000), (BPMPoint<200>, 2000), (BPMPoint<300>, 3000)]

        :param last_offset: If not None, then this offset will be used to terminate activity, else last offset will\
            be used.
        :return: A List of Tuples in the format [(BPMPoint, Activity In ms), ...]
        """
        return self.bpms.activity(last_offset if last_offset else self.notes.last_offset())

    def ave_bpm(self, last_offset: float = None) -> float:
        """ Calculates the average Bpm.

        :param last_offset: If not None, then this offset will be used to terminate activity, else last note offset will\
            be used.
        """
        activity_sum = 0
        sum_prod = 0
        for bpm, activity in self.activity(last_offset if last_offset else self.notes.last_offset()):
            activity_sum += activity
            sum_prod += bpm.bpm * activity
        return sum_prod / activity_sum

    def scroll_speed(self, reference_bpm: float = None) -> List[Dict[str, float]]:
        """ Evaluates the scroll speed based on mapType

        e.g. if BPM == 200.0 and CenterBPM == 100.0, it'll return {'offset': X, 'speed': 2.0}

        :param reference_bpm: The bpm to zero calculations on. If None, it'll just be the multiplication of bpm and sv.
        :return: Returns a list dict of keys offset and speed
        """

        # This automatically calculates the center BPM
        # Bpm Activity implicitly sorts
        if reference_bpm is None: reference_bpm = 1
        return [dict(offset=bpm.offset, speed=bpm.bpm / reference_bpm) for bpm in self.bpms]

    @abstractmethod
    def metadata(self, unicode=True, **kwargs) -> str:
        """ Grabs the map metadata

        :param unicode: Whether to try to find the unicode or non-unicode. \
            This doesn't try to convert unicode to ascii, it just looks for if there's an available translation.
        :return: A string containing the metadata
        """
        ...

    def describe(self, rounding: int = 2, unicode: bool = False, **kwargs) -> None:
        """ Describes the map's attributes as a short summary

        :param rounding: The decimal rounding
        :param unicode: Whether to attempt to get the non-unicode or unicode. \
            Doesn't attempt to translate.
        """
        print(f"Average BPM: {round(self.ave_bpm(), rounding)}")

        first, last = self.notes.first_last_offset()
        print(f"Map Length: {datetime.timedelta(milliseconds=last - first)}")
        print(self.metadata(unicode=unicode, **kwargs))
        print("---- NPS ----")
        self.notes.describe_notes()

    def rate(self, by: float) -> Map:
        """ Changes the rate of the map

        :param by: The value to rate it by. 1.1x speeds up the song by 10%. Hence 10/11 of the length.
        """

        # We invert it so it's easier to multiply
        by = 1 / by

        return self.mult_offset(by=by)

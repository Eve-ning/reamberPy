from typing import List
from reamber.base.Bpm import Bpm
from reamber.base.lists.TimedList import TimedList
from abc import ABC


class BpmList(List[Bpm], TimedList, ABC):
    """ A List that holds a list of Bpms, useful to do group Bpm operations """

    def data(self) -> List[Bpm]:
        """ Grabs the list of Bpm """
        return self

    def bpms(self) -> List[float]:
        """ Grabs a list of Bpm values only """
        return self.attribute('bpm')

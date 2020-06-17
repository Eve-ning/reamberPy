from typing import List
from reamber.base.BpmObj import BpmObj
from reamber.base.lists.TimedList import TimedList
from abc import ABC


class BpmList(List[BpmObj], TimedList, ABC):
    """ A List that holds a list of Bpms, useful to do group Bpm operations """

    def data(self) -> List[BpmObj]:
        """ Grabs the list of BpmObj """
        return self

    def bpms(self) -> List[float]:
        """ Grabs a list of Bpm values only """
        return self.attribute('bpm')

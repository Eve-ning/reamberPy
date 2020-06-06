from typing import List

from reamber.base.lists.BpmList import BpmList
from reamber.quaver.QuaBpmObj import QuaBpmObj


class QuaBpmList(BpmList):
    def data(self) -> List[QuaBpmObj]:
        return self

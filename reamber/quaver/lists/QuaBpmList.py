from typing import List

from reamber.base.lists.BpmList import BpmList
from reamber.quaver.QuaBpmObject import QuaBpmObject


class QuaBpmList(BpmList):
    def data(self) -> List[QuaBpmObject]:
        return self

from __future__ import annotations
from typing import List
from reamber.base.Hit import Hit
from abc import ABC, abstractmethod

class HitList(ABC):

    @abstractmethod
    def data(self) -> List[Hit]: ...


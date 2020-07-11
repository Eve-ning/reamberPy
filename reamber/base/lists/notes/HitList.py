from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from reamber.base.Hit import Hit


class HitList(ABC):

    @abstractmethod
    def data(self) -> List[Hit]: ...


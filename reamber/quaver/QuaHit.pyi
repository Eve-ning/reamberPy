from typing import Dict, List, Any

from reamber.base.Hit import Hit
from reamber.quaver.QuaNoteMeta import QuaNoteMeta


class QuaHit(Hit, QuaNoteMeta):

    def __init__(self, offset: float, column: int, keysounds: List[str],
                 **kwargs): ...

    def to_yaml(self) -> Dict[str, Any]: ...

    @staticmethod
    def from_yaml(d: Dict[str, Any]) -> QuaHit: ...

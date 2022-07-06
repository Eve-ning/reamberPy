from typing import Dict, List, Any

from reamber.base.Hold import Hold
from reamber.quaver.QuaNoteMeta import QuaNoteMeta


class QuaHold(QuaNoteMeta, Hold):

    def __init__(self, offset: float, column: int, length: float,
                 keysounds: List[str], **kwargs): ...

    def to_yaml(self) -> Dict[str, Any]: ...

    @staticmethod
    def from_yaml(d: Dict[str, Any]) -> QuaHold: ...

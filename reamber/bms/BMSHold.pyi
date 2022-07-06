from __future__ import annotations

from reamber.base.Hold import Hold
from reamber.bms.BMSNoteMeta import BMSNoteMeta


class BMSHold(Hold, BMSNoteMeta):
    def __init__(self, offset: float, column: int, length: float,
                 sample: bytes = b'', **kwargs): ...

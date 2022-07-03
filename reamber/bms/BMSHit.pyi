from __future__ import annotations

from reamber.base.Hit import Hit
from reamber.bms.BMSNoteMeta import BMSNoteMeta


class BMSHit(Hit, BMSNoteMeta):

    def __init__(self, offset: float, column: int, sample: bytes = b'',
                 **kwargs): ...

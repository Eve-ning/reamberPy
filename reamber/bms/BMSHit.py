from __future__ import annotations

from reamber.base import item_props
from reamber.base.Hit import Hit
from reamber.bms.BMSNoteMeta import BMSNoteMeta


@item_props()
class BMSHit(Hit, BMSNoteMeta):

    def __init__(self,
                 offset: float,
                 column: int,
                 sample: bytes = b'',
                 **kwargs):
        super().__init__(offset=offset, column=column, sample=sample, **kwargs)

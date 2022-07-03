from __future__ import annotations

from reamber.base import item_props
from reamber.base.Hold import Hold
from reamber.bms.BMSNoteMeta import BMSNoteMeta


@item_props()
class BMSHold(Hold, BMSNoteMeta):
    def __init__(self,
                 offset: float,
                 column: int,
                 length: float,
                 sample: bytes = b'',
                 **kwargs):
        super().__init__(offset=offset, column=column, length=length,
                         sample=sample, **kwargs)

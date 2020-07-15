from __future__ import annotations

from dataclasses import dataclass, field
from reamber.bms.BMSNoteMeta import BMSNoteMeta

from reamber.base.Hold import Hold, HoldTail


@dataclass
class BMSHoldTail(HoldTail, BMSNoteMeta):
    pass


@dataclass
class BMSHold(Hold, BMSNoteMeta):

    _tail: BMSHoldTail = field(init=False)

    def _upcastTail(self, **kwargs) -> BMSHoldTail:
        return BMSHoldTail(**kwargs)

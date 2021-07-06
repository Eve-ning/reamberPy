from __future__ import annotations

from dataclasses import dataclass, field

from reamber.base.Hold import Hold, HoldTail
from reamber.bms.BMSNoteMeta import BMSNoteMeta


@dataclass
class BMSHoldTail(HoldTail, BMSNoteMeta):
    pass


@dataclass
class BMSHold(Hold, BMSNoteMeta):

    _tail: BMSHoldTail = field(init=False)

    def _upcast_tail(self, **kwargs) -> BMSHoldTail:
        return BMSHoldTail(**kwargs)

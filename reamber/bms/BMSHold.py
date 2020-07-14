from __future__ import annotations

from dataclasses import dataclass, field

from reamber.base.Hold import Hold, HoldTail


@dataclass
class BMSHoldTail(HoldTail):
    pass


@dataclass
class BMSHold(Hold):

    _tail: BMSHoldTail = field(init=False)

    def _upcastTail(self, **kwargs) -> BMSHoldTail:
        return BMSHoldTail(**kwargs)

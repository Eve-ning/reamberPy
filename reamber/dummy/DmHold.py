from __future__ import annotations
from reamber.base.Hold import Hold, HoldTail
from dataclasses import dataclass, field


@dataclass
class DmHoldTail(HoldTail):
    pass


@dataclass
class DmHold(Hold):

    tail: DmHoldTail = field(init=False)

    def _upcastTail(self, **kwargs) -> DmHoldTail:
        return DmHoldTail(**kwargs)

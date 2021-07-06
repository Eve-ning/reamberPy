from __future__ import annotations

from dataclasses import dataclass, field

from reamber.base.Hold import Hold, HoldTail


@dataclass
class DmHoldTail(HoldTail):
    pass


@dataclass
class DmHold(Hold):

    _tail: DmHoldTail = field(init=False)

    def _upcast_tail(self, **kwargs) -> DmHoldTail:
        return DmHoldTail(**kwargs)

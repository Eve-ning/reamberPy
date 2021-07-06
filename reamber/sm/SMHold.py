from dataclasses import dataclass, field

from reamber.base.Hold import Hold, HoldTail


@dataclass
class SMHoldTail(HoldTail):
    pass


@dataclass
class SMHold(Hold):

    _tail: SMHoldTail = field(init=False)

    def _upcast_tail(self, **kwargs) -> SMHoldTail:
        return SMHoldTail(**kwargs)


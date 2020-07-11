from dataclasses import dataclass, field

from reamber.base.Hold import Hold, HoldTail


@dataclass
class SMRollTail(HoldTail):
    pass

@dataclass
class SMRoll(Hold):

    _tail: SMRollTail = field(init=False)

    def _upcastTail(self, **kwargs) -> SMRollTail:
        return SMRollTail(**kwargs)


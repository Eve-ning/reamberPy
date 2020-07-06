from dataclasses import dataclass, field
from reamber.base.Hold import Hold, HoldTail
from reamber.o2jam.O2JNoteMeta import O2JNoteMeta

@dataclass
class O2JHoldTail(HoldTail, O2JNoteMeta):
    pass


@dataclass
class O2JHold(Hold, O2JNoteMeta):
    """ Defines the O2Jam Bpm Object

    The O2Jam Bpm Object is stored in binary file .ojn
    """
    _tail: O2JHoldTail = field(init=False)

    def _upcastTail(self, **kwargs) -> O2JHoldTail:
        return O2JHoldTail(**kwargs)

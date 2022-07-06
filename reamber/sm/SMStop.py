from reamber.base import item_props
from reamber.base.Timed import Timed


@item_props()
class SMStop(Timed):
    _props = dict(length=['float', 0.0])

    def __init__(self, offset: float, length: float, **kwargs):
        super().__init__(offset=offset, length=length, **kwargs)

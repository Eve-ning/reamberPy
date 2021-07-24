from reamber.base import item_props
from reamber.base.Timed import Timed


@item_props()
class SMStop(Timed):

    _props = dict(length='float')

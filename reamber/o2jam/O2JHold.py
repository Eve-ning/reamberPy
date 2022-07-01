from reamber.base import item_props
from reamber.base.Hold import Hold
from reamber.o2jam.O2JNoteMeta import O2JNoteMeta


@item_props()
class O2JHold(Hold, O2JNoteMeta):

    def __init__(self,
                 offset: float,
                 column: int,
                 length: float,
                 volume: int = 0,
                 pan: int = 8,
                 **kwargs):
        super().__init__(
            offset=offset, column=column, length=length, volume=volume,
            pan=pan, **kwargs
        )

from reamber.base import item_props
from reamber.base.Hit import Hit
from reamber.o2jam.O2JNoteMeta import O2JNoteMeta


@item_props()
class O2JHit(Hit, O2JNoteMeta):

    def __init__(self,
                 offset: float,
                 column: int,
                 volume: int = 0,
                 pan: int = 8,
                 **kwargs):
        super().__init__(
            offset=offset, column=column, volume=volume, pan=pan, **kwargs
        )

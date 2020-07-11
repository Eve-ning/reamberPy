from dataclasses import dataclass

from reamber.base.Hit import Hit
from reamber.o2jam.O2JNoteMeta import O2JNoteMeta


@dataclass
class O2JHit(Hit, O2JNoteMeta):
    """ Defines the O2Jam Hit Object

    The O2Jam Hit Object is stored in binary file .ojn
    """
    pass

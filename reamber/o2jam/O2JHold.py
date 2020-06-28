from dataclasses import dataclass
from reamber.base.Hold import Hold
from reamber.o2jam.O2JNoteMeta import O2JNoteMeta


@dataclass
class O2JHold(Hold, O2JNoteMeta):
    """ Defines the O2Jam Bpm Object

    The O2Jam Bpm Object is stored in binary file .ojn
    """
    pass

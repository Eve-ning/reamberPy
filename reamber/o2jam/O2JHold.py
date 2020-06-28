from dataclasses import dataclass
from reamber.base.HoldObj import HoldObj
from reamber.o2jam.O2JNoteObjMeta import O2JNoteObjMeta


@dataclass
class O2JHoldObj(HoldObj, O2JNoteObjMeta):
    """ Defines the O2Jam Bpm Object

    The O2Jam Bpm Object is stored in binary file .ojn
    """
    pass

from dataclasses import dataclass
from reamber.base.HitObj import HitObj
from reamber.o2jam.O2JNoteObjMeta import O2JNoteObjMeta


@dataclass
class O2JHitObj(HitObj, O2JNoteObjMeta):
    """ Defines the O2Jam Hit Object

    The O2Jam Hit Object is stored in binary file .ojn
    """
    pass

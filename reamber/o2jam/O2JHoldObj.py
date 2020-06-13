from dataclasses import dataclass
from reamber.base.HoldObj import HoldObj
from reamber.o2jam.O2JNoteObjMeta import O2JNoteObjMeta


@dataclass
class O2JHoldObj(HoldObj, O2JNoteObjMeta):
    pass

from dataclasses import dataclass
from reamber.base.HoldObject import HoldObject
from reamber.o2jam.O2JNoteObjectMeta import O2JNoteObjectMeta


@dataclass
class O2JHoldObject(HoldObject, O2JNoteObjectMeta):
    INT_HEAD: int = 2
    INT_TAIL: int = 3

from dataclasses import dataclass
from reamber.base.HitObject import HitObject
from reamber.o2jam.O2JNoteObjectMeta import O2JNoteObjectMeta


@dataclass
class O2JHitObject(HitObject, O2JNoteObjectMeta):
    INT     : int  = 0  # This is the character used to indicate the note type

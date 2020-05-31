from dataclasses import dataclass
from reamber.base.HitObject import HitObject


@dataclass
class O2JNoteObjectMeta:
    volume  : int  = 0
    pan     : int  = 8  # 0 or 8 is center pan


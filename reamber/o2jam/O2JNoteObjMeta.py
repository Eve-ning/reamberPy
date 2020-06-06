from dataclasses import dataclass


@dataclass
class O2JNoteObjMeta:
    volume  : int  = 0
    pan     : int  = 8  # 0 or 8 is center pan


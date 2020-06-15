from dataclasses import dataclass


@dataclass
class O2JNoteObjMeta:
    """ Metadata of a O2Jam Note. """

    volume  : int  = 0
    pan     : int  = 8  # 0 or 8 is center pan


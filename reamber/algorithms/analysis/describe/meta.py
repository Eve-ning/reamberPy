from reamber.base.MapObject import MapObject
from reamber.osu.OsuMapObject import OsuMapObject
from reamber.sm.SMMapSetObject import SMMapSetObject, SMMapObject
from reamber.quaver.QuaMapObject import QuaMapObject
from typing import overload


@overload
def mapMetadata(m: OsuMapObject, s: None, unicode: bool) -> str: ...
@overload
def mapMetadata(m: QuaMapObject, s: None, unicode: bool) -> str: ...
@overload
def mapMetadata(m: SMMapObject, s: SMMapSetObject, unicode: bool) -> str: ...
def mapMetadata(m, s, unicode=True) -> str:
    def formatting(artist, title, difficulty): return f"{artist} - {title}, {difficulty}"
    if isinstance(m, OsuMapObject):
        if unicode: return formatting(m.artistUnicode, m.titleUnicode, m.version)
        else: return formatting(m.artist, m.title, m.version)
    elif isinstance(m, QuaMapObject):
        return formatting(m.artist, m.title, m.difficultyName)
    elif isinstance(m, SMMapObject) and isinstance(s, SMMapSetObject):
        if unicode: return formatting(s.artist if len(s.artist) > 0 else s.artistTranslit,
                                      s.title if len(s.title) > 0 else s.title,
                                      m.difficulty)
    else:
        raise NotImplementedError

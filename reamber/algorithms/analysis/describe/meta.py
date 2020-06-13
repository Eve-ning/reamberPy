from reamber.o2jam.O2JMapSetObj import O2JMapSetObj, O2JMapObj
from reamber.osu.OsuMapObj import OsuMapObj
from reamber.sm.SMMapSetObj import SMMapSetObj, SMMapObj
from reamber.quaver.QuaMapObj import QuaMapObj
from typing import overload


@overload
def mapMetadata(m: O2JMapObj, s: O2JMapSetObj, unicode: bool) -> str: ...
@overload
def mapMetadata(m: OsuMapObj, s: None, unicode: bool) -> str: ...
@overload
def mapMetadata(m: QuaMapObj, s: None, unicode: bool) -> str: ...
@overload
def mapMetadata(m: SMMapObj, s: SMMapSetObj, unicode: bool) -> str: ...
def mapMetadata(m, s, unicode=True) -> str:
    def formatting(artist, title, difficulty): return f"{artist} - {title}, {difficulty}"
    if isinstance(m, OsuMapObj):
        if unicode: return formatting(m.artistUnicode, m.titleUnicode, m.version)
        else: return formatting(m.artist, m.title, m.version)

    elif isinstance(m, QuaMapObj):
        return formatting(m.artist, m.title, m.difficultyName)

    elif isinstance(m, SMMapObj) and isinstance(s, SMMapSetObj):
        if unicode: return formatting(s.artist if len(s.artist.strip()) > 0 else s.artistTranslit,
                                      s.title if len(s.title.strip()) > 0 else s.titleTranslit,
                                      m.difficulty)
        else: return formatting(s.artistTranslit if len(s.artistTranslit.strip()) > 0 else s.artist,
                                s.titleTranslit if len(s.titleTranslit.strip()) > 0 else s.title,
                                m.difficulty)

    elif isinstance(m, O2JMapObj) and isinstance(s, O2JMapSetObj):
        try:
            return formatting(s.artist.strip(), s.title, f"Level {s.level[s.maps.index(m)]}")
        except IndexError:
            return formatting(s.artist, s.title, "Cannot determine level")
        
    else:
        raise NotImplementedError

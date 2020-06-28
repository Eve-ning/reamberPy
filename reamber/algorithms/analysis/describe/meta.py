from reamber.o2jam.O2JMapSetObj import O2JMapSetObj, O2JMapObj
from reamber.osu.OsuMapObj import OsuMapObj
from reamber.sm.SMMapSetObj import SMMapSetObj, SMMapObj
from reamber.quaver.QuaMapObj import QuaMapObj
from typing import overload


@overload
def mapMetadata(m: O2JMapObj, s: O2JMapSetObj = None, unicode: bool = True) -> str: ...
@overload
def mapMetadata(m: OsuMapObj, s: None = None, unicode: bool = True) -> str: ...
@overload
def mapMetadata(m: QuaMapObj, s: None = None, unicode: bool = True) -> str: ...
@overload
def mapMetadata(m: SMMapObj, s: SMMapSetObj = None, unicode: bool = True) -> str: ...
def mapMetadata(m, s=None, unicode=True) -> str:
    """ Grabs the map metadata

    :param m: The Map Object
    :param s: The Map Set Object, not required for some types
    :param unicode: Whether to try to find the unicode or non-unicode. \
        This doesn't try to convert unicode to ascii, it just looks for if there's an available translation.
    :return:
    """
    def formatting(artist, title, difficulty, creator): return f"{artist} - {title}, {difficulty} ({creator})"
    if isinstance(m, OsuMapObj):
        if unicode: return formatting(m.artistUnicode, m.titleUnicode, m.version, m.creator)
        else: return formatting(m.artist, m.title, m.version, m.creator)

    elif isinstance(m, QuaMapObj):
        return formatting(m.artist, m.title, m.difficultyName, m.creator)

    elif isinstance(m, SMMapObj) and isinstance(s, SMMapSetObj):
        if unicode: return formatting(s.artist if len(s.artist.strip()) > 0 else s.artistTranslit,
                                      s.title if len(s.title.strip()) > 0 else s.titleTranslit,
                                      m.difficulty, s.credit)
        else: return formatting(s.artistTranslit if len(s.artistTranslit.strip()) > 0 else s.artist,
                                s.titleTranslit if len(s.titleTranslit.strip()) > 0 else s.title,
                                m.difficulty, s.credit)

    elif isinstance(m, O2JMapObj) and isinstance(s, O2JMapSetObj):
        try:
            return formatting(s.artist.strip(), s.title, f"Level {s.level[s.maps.index(m)]}", s.creator)
        except IndexError:
            return formatting(s.artist, s.title, "Cannot determine level", s.creator)
        
    else:
        raise NotImplementedError

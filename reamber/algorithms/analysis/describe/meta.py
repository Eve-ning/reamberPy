from reamber.o2jam.O2JMapSet import O2JMapSet, O2JMap
from reamber.osu.OsuMap import OsuMap
from reamber.sm.SMMapSet import SMMapSet, SMMap
from reamber.quaver.QuaMap import QuaMap
from typing import overload


@overload
def mapMetadata(m: O2JMap, s: O2JMapSet = None, unicode: bool = True) -> str: ...
@overload
def mapMetadata(m: OsuMap, s: None = None, unicode: bool = True) -> str: ...
@overload
def mapMetadata(m: QuaMap, s: None = None, unicode: bool = True) -> str: ...
@overload
def mapMetadata(m: SMMap, s: SMMapSet = None, unicode: bool = True) -> str: ...
def mapMetadata(m, s=None, unicode=True) -> str:
    """ Grabs the map metadata

    :param m: The Map Object
    :param s: The Map Set Object, not required for some types
    :param unicode: Whether to try to find the unicode or non-unicode. \
        This doesn't try to convert unicode to ascii, it just looks for if there's an available translation.
    :return:
    """
    def formatting(artist, title, difficulty, creator): return f"{artist} - {title}, {difficulty} ({creator})"
    if isinstance(m, OsuMap):
        if unicode: return formatting(m.artistUnicode, m.titleUnicode, m.version, m.creator)
        else: return formatting(m.artist, m.title, m.version, m.creator)

    elif isinstance(m, QuaMap):
        return formatting(m.artist, m.title, m.difficultyName, m.creator)

    elif isinstance(m, SMMap) and isinstance(s, SMMapSet):
        if unicode: return formatting(s.artist if len(s.artist.strip()) > 0 else s.artistTranslit,
                                      s.title if len(s.title.strip()) > 0 else s.titleTranslit,
                                      m.difficulty, s.credit)
        else: return formatting(s.artistTranslit if len(s.artistTranslit.strip()) > 0 else s.artist,
                                s.titleTranslit if len(s.titleTranslit.strip()) > 0 else s.title,
                                m.difficulty, s.credit)

    elif isinstance(m, O2JMap) and isinstance(s, O2JMapSet):
        try:
            return formatting(s.artist.strip(), s.title, f"Level {s.level[s.maps.index(m)]}", s.creator)
        except IndexError:
            return formatting(s.artist, s.title, "Cannot determine level", s.creator)
        
    else:
        raise NotImplementedError

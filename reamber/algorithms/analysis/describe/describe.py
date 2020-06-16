from reamber.base.lists.NotePkg import NotePkg
from typing import overload
from reamber.algorithms.analysis.bpm.aveBpm import aveBpm
from reamber.algorithms.analysis.generic.rollingDensity import rollingDensity
from reamber.algorithms.analysis.describe.meta import mapMetadata

from reamber.o2jam.O2JMapSetObj import O2JMapSetObj, O2JMapObj
from reamber.osu.OsuMapObj import OsuMapObj
from reamber.sm.SMMapSetObj import SMMapSetObj, SMMapObj
from reamber.quaver.QuaMapObj import QuaMapObj

from reamber.o2jam.lists.O2JNotePkg import O2JNotePkg
from reamber.osu.lists.OsuNotePkg import OsuNotePkg
from reamber.sm.lists.SMNotePkg import SMNotePkg
from reamber.quaver.lists.QuaNotePkg import QuaNotePkg
import datetime


@overload
def describe(m: O2JMapObj, s: O2JMapSetObj) -> None: ...
@overload
def describe(m: OsuMapObj, s: None) -> None: ...
@overload
def describe(m: QuaMapObj, s: None) -> None: ...
@overload
def describe(m: SMMapObj, s: SMMapSetObj) -> None: ...
def describe(m: QuaMapObj, s, rounding: int = 2, unicode: bool = False) -> None:
    """ Describes the map's attributes as a short summary

    :param m: The map
    :param s: The mapset, may be optional for some types
    :param rounding: The decimal rounding
    :param unicode: Whether to attempt to get the non-unicode or unicode. \
        Doesn't attempt to translate.
    """
    print(f"Average BPM: {round(aveBpm(m), rounding)}")

    first, last = m.notes.firstLastOffset()
    print(f"Map Length: {datetime.timedelta(milliseconds=last - first)}")
    # noinspection PyTypeChecker
    print(mapMetadata(m=m, s=s, unicode=unicode))
    print("---- NPS ----")
    print("All:", end='  ')
    describeNotes(m.notes)
    for key in range(m.notes.maxColumn() + 1):
        print(f"Col{key}:", end=' ')
        describeNotes(m.notes.inColumns([key], inplace=False))
    pass

@overload
def describeNotes(notePkg: OsuNotePkg, rounding: int = 2): ...
@overload
def describeNotes(notePkg: SMNotePkg, rounding: int = 2): ...
@overload
def describeNotes(notePkg: QuaNotePkg, rounding: int = 2): ...
@overload
def describeNotes(notePkg: O2JNotePkg, rounding: int = 2): ...
def describeNotes(notePkg: NotePkg, rounding: int = 2):
    """ Describes a single NotePkg

    Prints out Count, Median, 75% quantile and max

    :param notePkg: Any Note Package
    :param rounding: The decimal rounding
    """
    # This is fixed to be 1 for consistency in value
    sr = rollingDensity([i for j in notePkg.offsets().values() for i in j], rollingWindowS=1)
    print(       f"Count: {len([i for j in notePkg.offsets().values() for i in j])}, "
          f"50% (Median): {float(sr.quantile(0.5)):.{rounding}f}, "
                   f"75%: {float(sr.quantile(0.75)):.{rounding}f}, "
            f"100% (Max): {float(sr.max()):.{rounding}f}")


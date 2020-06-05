from reamber.base.MapObject import MapObject
from plotnine import *
from reamber.base.mapobj.MapObjectNotes import MapObjectNotes
from reamber.base.mapobj.MapObjectBase import MapObjectBase
from typing import List, Type, overload
import reamber.algorithms.analysis as anl
from reamber.algorithms.analysis.describe.meta import mapMetadata

from reamber.osu.OsuMapObject import OsuMapObject
from reamber.sm.SMMapSetObject import SMMapSetObject, SMMapObject
from reamber.quaver.QuaMapObject import QuaMapObject
import datetime

@overload
def describePrint(m: OsuMapObject, s: None) -> None: ...
@overload
def describePrint(m: QuaMapObject, s: None) -> None: ...
@overload
def describePrint(m: SMMapObject, s: SMMapSetObject) -> None: ...
def describePrint(m: QuaMapObject, s, rounding:int = 2, unicode:bool = False) -> None:
    """ Describes the map's attributes as a short summary """

    print(f"Average BPM: {round(anl.aveBpm(m), rounding)}")

    first, last = m.notes.firstLastOffset()
    print(f"Map Length: {datetime.timedelta(milliseconds=last - first)}")
    # noinspection PyTypeChecker
    print(mapMetadata(m=m, s=s, unicode=unicode))
    print("---- NPS ----")
    print("All:", end='  ')
    describeNotes(m.notes)
    for key in range(m.notes.maxColumns() + 1):
        print(f"Col{key}:", end=' ')
        describeNotes(m.notes.inColumns([key]))
    pass


def describeNotes(m: Type[MapObjectBase], rounding: int = 2):
    sr = anl.rollingDensity(m, rollingWindowS=1)  # This is fixed to be 1 for consistency in value
    print(       f"Count: {len(m)}, "
          f"50% (Median): {float(sr.quantile(0.5)):.{rounding}f}, "
                   f"75%: {float(sr.quantile(0.75)):.{rounding}f}, "
            f"100% (Max): {float(sr.max()):.{rounding}f}, "
              f"Variance: {float(sr.var()):.{rounding}f}")


def describePlot(m: MapObject, rollingWindowS: int = 5):
    """ This is the more in-depth describe 
    In this, we will mainly pivot on graphs
    :param m: The MapObject or any variant
    :param rollingWindowS: The window of rolling() in seconds. A larger value means a smoother plot

    """

    df = anl.rollingDensity(m.notes, rollingWindowS=rollingWindowS)
    df.reset_index(level=0, inplace=True)
    df['offset'] = df['offset'].dt.total_seconds()
    print(ggplot(df, aes({'x': 'offset', 'y': 'count'}))
          + geom_point()
          + geom_smooth(span=1))

    # register_matplotlib_converters()
    # plt.style.use('dark_background')
    #
    # plt.plot(anl.rollingDensity(m.noteObjects, rollingWindowS=5), label="Total NPS")
    # plt.plot(anl.rollingDensity(m.hitObjects(), rollingWindowS=5), label="Hit Objects")
    # plt.plot(anl.rollingDensity(m.holdObjects(), rollingWindowS=5), label="Hold Objects")
    # plt.xlabel("duration")
    # plt.ylabel("notes per second")
    # plt.legend()
    # plt.show()

from reamber.base.MapObj import MapObj
from plotnine import *
from reamber.base.lists.NotePkg import NotePkg
from reamber.base.lists.TimedList import TimedList
from typing import Type, overload
import reamber.algorithms.analysis as anl
from reamber.algorithms.analysis.describe.meta import mapMetadata

from reamber.osu.OsuMapObj import OsuMapObj
from reamber.sm.SMMapSetObj import SMMapSetObj, SMMapObj
from reamber.quaver.QuaMapObj import QuaMapObj
import datetime


@overload
def describePrint(m: OsuMapObj, s: None) -> None: ...
@overload
def describePrint(m: QuaMapObj, s: None) -> None: ...
@overload
def describePrint(m: SMMapObj, s: SMMapSetObj) -> None: ...
def describePrint(m: QuaMapObj, s, rounding: int = 2, unicode: bool = False) -> None:
    """ Describes the map's attributes as a short summary """

    print(f"Average BPM: {round(anl.aveBpm(m), rounding)}")

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


def describeNotes(m: NotePkg, rounding: int = 2):
    # This is fixed to be 1 for consistency in value
    sr = anl.rollingDensity([i for j in m.offsets().values() for i in j], rollingWindowS=1)
    print(       f"Count: {len([i for j in m.offsets().values() for i in j])}, "
          f"50% (Median): {float(sr.quantile(0.5)):.{rounding}f}, "
                   f"75%: {float(sr.quantile(0.75)):.{rounding}f}, "
            f"100% (Max): {float(sr.max()):.{rounding}f}, "
              f"Variance: {float(sr.var()):.{rounding}f}")

@overload
def describePlot(m: OsuMapObj) -> None: ...
@overload
def describePlot(m: QuaMapObj) -> None: ...
@overload
def describePlot(m: SMMapObj) -> None: ...
def describePlot(m: QuaMapObj):
    """ This is the more in-depth describe 
    In this, we will mainly pivot on graphs
    :param m: The MapObj or any variant
    :param rollingWindowS: The window of rolling() in seconds. A larger value means a smoother plot

    """

    df25 = anl.rollingDensity([i for j in m.notes.offsets().values() for i in j], rollingWindowS=25)
    df10 = anl.rollingDensity([i for j in m.notes.offsets().values() for i in j], rollingWindowS=10)
    df25 = df25.reset_index()
    df25['offset'] = df25['offset'].dt.total_seconds()
    df10 = df10.reset_index()
    df10['offset'] = df10['offset'].dt.total_seconds()
    print(ggplot() +
          geom_area(data=df25, alpha=0.5, color='blue', fill='blue ', mapping=aes(x='offset', y='count')) +
          geom_area(data=df10, color='green', fill='green', alpha=0.4, mapping=aes(x='offset', y='count')))

    # register_matplotlib_converters()
    # plt.style.use('dark_background')
    #
    # plt.plot(anl.rollingDensity(m.noteObjs, rollingWindowS=5), label="Total NPS")
    # plt.plot(anl.rollingDensity(m.hitObjs(), rollingWindowS=5), label="Hit Objs")
    # plt.plot(anl.rollingDensity(m.holdObjs(), rollingWindowS=5), label="Hold Objs")
    # plt.xlabel("duration")
    # plt.ylabel("notes per second")
    # plt.legend()
    # plt.show()

from reamber.base.MapObj import MapObj
from plotnine import *
from reamber.base.lists.NotePkg import NotePkg
from reamber.base.lists.TimedList import TimedList
from typing import List, overload
import reamber.algorithms.analysis as anl
from reamber.algorithms.analysis.describe.meta import mapMetadata

import pandas as pd

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
            f"100% (Max): {float(sr.max()):.{rounding}f}")

@overload
def describePlot(m: OsuMapObj, smoothFactor: float = 0.01) -> None: ...
@overload
def describePlot(m: QuaMapObj, smoothFactor: float = 0.01) -> None: ...
@overload
def describePlot(m: SMMapObj, smoothFactor: float = 0.01) -> None: ...
def describePlot(m: QuaMapObj, smoothFactor: float = 0.01):
    """ This is the more in-depth describe 
    In this, we will mainly pivot on graphs
    :param m: The MapObj or any variant
    :param smoothFactor: How smooth is it, between 0 and 1, not inclusive

    """

    assert 0 < smoothFactor < 1, "Smooth Factor must be between 0 and 1"

    theme_set(theme_minimal())

    df = anl.rollingDensity([i for j in m.notes.offsets().values() for i in j], rollingWindowS=1)
    df = df.reset_index()
    df['offset'] = df['offset'].dt.total_seconds()

    plot = ggplot(df, aes(x='offset', y='count')) +\
           ylab("NPS") +\
           geom_smooth(method='mavg', method_args={'window': int(len(df) * smoothFactor)}, se=False)

    print(plot)


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

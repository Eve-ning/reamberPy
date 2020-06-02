from reamber.base.MapObject import MapObject
from plotnine import *
from reamber.base.NoteObject import NoteObject
from typing import List
import reamber.algorithms.analysis as anl
import datetime


def describePrint(m: MapObject, rounding=2):
    """ Describes the map's attributes as a short summary """

    print(f"Average BPM: {round(anl.aveBpm(m), rounding)}")

    first, last = m.notes.firstLastNoteOffset()
    print(f"Map Length: {datetime.timedelta(milliseconds=last - first)}")

    print("---- NPS ----")
    print("All:", end='  ')
    describeNotes(m.notes)
    for key in range(m.notes.keys() + 1):
        print(f"Col{key}:", end=' ')
        describeNotes([note for note in m.notes if note.column == key])
    pass


def describeNotes(notes: List[NoteObject], rounding: int = 2):
    df = anl.rollingDensity(notes, rollingWindowS=1)  # This is fixed to be 1 for consistency in value
    print(       f"Count: {len(notes)}, "
          f"50% (Median): {float(df.quantile(0.5)):.{rounding}f}, "
                   f"75%: {float(df.quantile(0.75)):.{rounding}f}, "
            f"100% (Max): {float(df.max()):.{rounding}f}, "
              f"Variance: {float(df.var()):.{rounding}f}")


def describePlot(m: MapObject, rollingWindowS: int = 5):
    """ This is the more in-depth describe 
    In this, we will mainly pivot on graphs
    :param m: The MapObject or any variant
    :param rollingWindowS: The window of rolling() in seconds. A larger value means a smoother plot

    """

    df = anl.rollingDensity(m.notes, rollingWindowS=rollingWindowS)
    df.reset_index(level=0, inplace=True)
    df['offset'] = df['offset'].dt.total_seconds()
    print(ggplot(df, aes(x='offset', y='count'))
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

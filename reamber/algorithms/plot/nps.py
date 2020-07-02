import matplotlib.pyplot as plt
import matplotlib.axes as axes
from typing import overload

from reamber.osu.OsuMap import OsuMap
from reamber.sm.SMMapSet import SMMap
from reamber.o2jam.O2JMap import O2JMap
from reamber.quaver.QuaMap import QuaMap

@overload
def npsPlot(m: O2JMap, widthPx=1000, heightPx=200, dpi=100, binSize=1000) -> None: ...
@overload
def npsPlot(m: OsuMap, widthPx=1000, heightPx=200, dpi=100, binSize=1000) -> None: ...
@overload
def npsPlot(m: QuaMap, widthPx=1000, heightPx=200, dpi=100, binSize=1000) -> None: ...
@overload
def npsPlot(m: SMMap, widthPx=1000, heightPx=200, dpi=100, binSize=1000) -> None: ...
def npsPlot(m: SMMap, widthPx=1000, heightPx=200, dpi=100, binSize=1000) -> None:
    """ This creates an NPS plot. The peaks and troughs may differ depending on binSize

    :param dpi: dpi
    :param heightPx: Height in pixels
    :param widthPx: Width in pixels
    :param m: The Map or any variant
    :param binSize: The size of the binning
    """
    df = m.nps(binSize=binSize)
    df.set_index(df['offset'], inplace=True)
    df.drop('offset', axis='columns', inplace=True)
    subplot = df.plot(kind='bar', stacked=True, width=1.0)
    ax: axes.Axes = subplot.axes
    ax.set_xticks([])
    ax.set_ylabel("NPS")
    ax.set_xlabel("")
    fig = ax.get_figure()
    fig.set_size_inches(widthPx / dpi, heightPx / dpi)
    plt.tight_layout()


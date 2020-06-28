import matplotlib.pyplot as plt
import matplotlib.axes as axes
from typing import overload

import pandas as pd

from reamber.osu.OsuMap import OsuMap
from reamber.sm.SMMapSet import SMMap
from reamber.o2jam.O2JMap import O2JMap
from reamber.quaver.QuaMap import QuaMap

@overload
def nps(m: O2JMap, binSize: int = 1000) -> pd.DataFrame: ...
@overload
def nps(m: OsuMap, binSize: int = 1000) -> pd.DataFrame: ...
@overload
def nps(m: QuaMap, binSize: int = 1000) -> pd.DataFrame: ...
@overload
def nps(m: SMMap, binSize: int = 1000) -> pd.DataFrame: ...
def nps(m: SMMap, binSize: int = 1000) -> pd.DataFrame:
    """ Gets the NPS as a DataFrame

    :param m: The Map or any variant
    :param binSize: The size of the binning
    """

    dfMaster = None

    for k, l in m.notes.data().items():
        if len(l.data()) == 0: continue
        # Fence post issue, last offset will be cut short, so we add a bin to cover the end
        dfCut = pd.cut(l.df()['offset'], bins=list(range(0, int(l.lastOffset()) + binSize, binSize)))
        dfCut = dfCut.groupby(dfCut).count()
        df = pd.DataFrame({f"{k}": dfCut.values / (binSize / 1000)})
        df = df.reset_index(inplace=False).rename(columns={'index': 'offset'}, inplace=False)
        df['offset'] *= binSize
        if dfMaster is None: dfMaster = df
        else: dfMaster = dfMaster.merge(df)

    return dfMaster

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
    df = nps(m, binSize=binSize)
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


import matplotlib.pyplot as plt
import matplotlib.axes as axes
from typing import overload

import pandas as pd

from reamber.osu.OsuMapObj import OsuMapObj
from reamber.sm.SMMapSetObj import SMMapObj
from reamber.o2jam.O2JMapObj import O2JMapObj
from reamber.quaver.QuaMapObj import QuaMapObj

@overload
def nps(m: O2JMapObj, binSize: int = 1000) -> pd.DataFrame: ...
@overload
def nps(m: OsuMapObj, binSize: int = 1000) -> pd.DataFrame: ...
@overload
def nps(m: QuaMapObj, binSize: int = 1000) -> pd.DataFrame: ...
@overload
def nps(m: SMMapObj, binSize: int = 1000) -> pd.DataFrame: ...
def nps(m: SMMapObj, binSize: int = 1000) -> pd.DataFrame:
    """ Gets the NPS as a DataFrame

    :param m: The MapObj or any variant
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
def npsPlot(m: O2JMapObj, filePath: str or None, widthPx=1000, heightPx=200, dpi=100, binSize=1000) -> None: ...
@overload
def npsPlot(m: OsuMapObj, filePath: str or None, widthPx=1000, heightPx=200, dpi=100, binSize=1000) -> None: ...
@overload
def npsPlot(m: QuaMapObj, filePath: str or None, widthPx=1000, heightPx=200, dpi=100, binSize=1000) -> None: ...
@overload
def npsPlot(m: SMMapObj, filePath: str or None, widthPx=1000, heightPx=200, dpi=100, binSize=1000) -> None: ...
def npsPlot(m: SMMapObj, filePath: str or None, widthPx=1000, heightPx=200, dpi=100, binSize=1000) -> None:
    """ This creates an NPS plot. The peaks and troughs may differ depending on binSize

    :param dpi: dpi
    :param heightPx: Height in pixels
    :param widthPx: Width in pixels
    :param filePath: The file path to export the plot, None if you don't want to export
    :param m: The MapObj or any variant
    :param binSize: The size of the binning
    """
    plt.tight_layout()
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
    if filePath is not None: fig.savefig(filePath, dpi=dpi)

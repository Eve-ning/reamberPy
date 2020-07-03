import matplotlib.pyplot as plt
import numpy as np

from typing import Tuple, List
from math import ceil

from reamber.base.lists.NotePkg import NotePkg
from reamber.base.RAConst import RAConst
from reamber.algorithms.plot.timedXAxis import timedXAxis

def npsPlot(pkg: NotePkg, ax:plt.Axes = None, window=1000, stride=None, legend=True, barKwargs=None) -> plt.Axes:
    """ This creates an NPS Plot with the axes.

    :param pkg: Any Note Package
    :param ax: The axis to plot on, if None, we use gca()
    :param window: The window of the roll
    :param stride: The stride length of the roll
    :param legend: Whether to show the legend
    :param barKwargs: The kwargs to pass into plot()
    """
    if ax is None: ax = plt.gca()
    if barKwargs is None: barKwargs = {}
    dns = pkg.rollingDensity(window=window, stride=stride)

    prevHeights = None
    for lisType, lis in dns.items():
        if all(v == 0 for v in lis.values()): continue
        currIndexes = list(lis.keys())
        currHeights = [RAConst.secToMSec(v / window) for v in list(lis.values())]
        ax.bar(currIndexes, currHeights,
               width=pkg.duration() / (len(lis.keys()) - 1),  # -1 to make sure there's no gaps
               bottom=prevHeights,  # Aligns next bar heights with previous
               label=lisType,
               **barKwargs)  # Aligns the bars next to each other
        prevHeights = currHeights
    if legend: ax.legend()
    ax.set_xlim(left=pkg.firstOffset(), right=pkg.lastOffset())
    ax = timedXAxis(ax=ax, stepSize=15000)
    return ax

def npsPlotByKey(pkg: NotePkg, fig:plt.Figure = None, shape: Tuple = None,
                 window=1000, stride=None, title=True, legend=True, barKwargs=None) -> plt.Figure:
    """ This creates an NPS Plot with the axes.

    :param pkg: Any Note Package
    :param fig: The figure to plot on, if None, we use gcf()
    :param shape: The shape of the axes to take. (rows, columns)
    :param window: The window of the roll
    :param stride: The stride length of the roll
    :param title: Whether to show the key titles
    :param legend: Whether to show legend. False to show none, True to show on first, 'all' to show on all
    :param barKwargs: The kwargs to pass into plot()
    """
    if fig is None: fig = plt.gcf()
    if barKwargs is None: barKwargs = {}

    keys = pkg.maxColumn() + 1  # This gives us the keys
    if shape is None:
        rows = ceil(keys ** 0.5)
        cols = int(keys / rows)
        shape = (rows, cols)
    else:
        assert shape[0] * shape[1] >= keys, "Shape must be able to hold all keys."

    ax: np.ndarray = fig.subplots(nrows=shape[0], ncols=shape[1],
                                  sharex='all', sharey='all')
    ax = ax.flatten()

    for key in range(keys):
        if legend == 'all':
            npsPlot(pkg.inColumns([key]), ax=ax[key], window=window, stride=stride, legend=True, barKwargs=barKwargs)
        elif legend is True and key == 0:
            npsPlot(pkg.inColumns([key]), ax=ax[key], window=window, stride=stride, legend=True, barKwargs=barKwargs)
        else:
            npsPlot(pkg.inColumns([key]), ax=ax[key], window=window, stride=stride, legend=False, barKwargs=barKwargs)

        ax: List[plt.Axes]
        if title: ax[key].set_title(f"Key: {key}")

    fig.tight_layout()
    return fig
